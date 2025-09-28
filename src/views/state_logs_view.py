"""State logs view for displaying TimescaleDB state_logs table data."""

import asyncio
import asyncpg
import logging
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from textual.widgets import Button, Label, Static, LoadingIndicator, Tree
from textual.containers import Vertical, Horizontal, VerticalScroll, Container
from textual.reactive import reactive
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets.tree import TreeNode
from ..config import config

# Set up file-based logging
logging.basicConfig(
    filename='/tmp/panopticon_state_logs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('StateLogsView')


class StateCard(Container):
    """A card widget for displaying a single state entry as a tree."""

    DEFAULT_CSS = """
    StateCard {
        background: $boost;
        border: solid $primary;
        margin: 1;
        padding: 1;
        height: auto;
    }

    .card-header {
        text-style: bold;
        color: $warning;
        margin-bottom: 1;
    }

    Tree {
        height: auto;
        background: transparent;
    }
    """

    def __init__(self, state_num: int, timestamp: str, state_data: Dict[str, Any]) -> None:
        """Initialize a state card.

        Args:
            state_num: State number
            timestamp: Timestamp string
            state_data: Nested state data dictionary
        """
        super().__init__()
        self.state_num = state_num
        self.timestamp = timestamp
        self.state_data = state_data

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static(f"════ STATE #{self.state_num} @ {self.timestamp} ════", classes="card-header")

        # Create tree for state data
        tree: Tree = Tree("State")
        tree.root.expand()

        # Add all top-level keys to the tree
        for key in sorted(self.state_data.keys()):
            self._add_node(tree.root, key, self.state_data[key])

        yield tree

    def _add_node(self, parent: TreeNode, key: str, value: Any, indent: int = 0) -> None:
        """Recursively add nodes to the tree."""
        if isinstance(value, dict):
            if not value:
                # Empty dict
                node = parent.add(f"[cyan]{key}[/cyan]: [dim](empty)[/dim]")
            else:
                # Add expandable node for nested dict
                node = parent.add(f"[cyan]{key}[/cyan]")
                node.expand()  # Auto-expand first level
                # Recursively add children
                for k in sorted(value.keys()):
                    self._add_node(node, k, value[k], indent + 1)
        elif isinstance(value, list):
            # Handle arrays
            node = parent.add(f"[cyan]{key}[/cyan]: Array[{len(value)}]")
            if value and indent < 3:  # Limit expansion depth
                node.expand()
                for i, item in enumerate(value):
                    self._add_node(node, f"[{i}]", item, indent + 1)
        else:
            # Leaf node - display value
            if value is None:
                display_value = "[dim]null[/dim]"
            elif isinstance(value, bool):
                display_value = f"[green]{str(value).lower()}[/green]"
            elif isinstance(value, (int, float)):
                display_value = f"[yellow]{value}[/yellow]"
            else:
                display_value = f"[white]{value}[/white]"

            parent.add(f"[cyan]{key}[/cyan]: {display_value}")


class StateLogsView(Vertical):
    """Display state logs from TimescaleDB with manual refresh and export."""

    DEFAULT_CSS = """
    StateLogsView {
        height: 100%;
        width: 100%;
    }

    #controls {
        dock: top;
        height: auto;
        background: $panel;
        border-bottom: solid $primary;
    }

    #controls Horizontal {
        height: auto;
        padding: 0 0;
        margin: 1 0;
    }

    #controls Button {
        width: auto;
        height: auto;
        margin: 0 1;
        min-width: 10;
    }

    #status {
        margin: 0 2;
        color: $text;
        width: auto;
        height: auto;
    }

    #scroll-container {
        height: 1fr;
        width: 100%;
        overflow-y: auto;
    }

    LoadingIndicator {
        margin: 4 0;
        height: 5;
    }
    """

    # Reactive properties
    loading = reactive(False)
    status_text = reactive("Ready")

    def __init__(self):
        """Initialize the state logs view."""
        super().__init__()
        self.conn: Optional[asyncpg.Connection] = None
        self.last_error = None
        self.state_data = []  # Store fetched data
        self.cards = []  # Store card widgets

    def compose(self) -> ComposeResult:
        """Create child widgets for the view."""
        # Control panel with buttons
        with Horizontal(id="controls"):
            yield Button("Refresh", id="refresh-btn", variant="primary")
            yield Button("Export", id="export-btn", variant="success")
            yield Label("Ready", id="status")

        # Scrollable container for cards
        yield VerticalScroll(id="scroll-container")

    async def on_mount(self) -> None:
        """Handle widget mounting - connect to database and load initial data."""
        try:
            # Connect to database
            await self.connect_db()

            # Load initial data (10 latest records)
            await self.load_data()

        except Exception as e:
            self.show_error(f"Failed to initialize: {e}")
            import traceback
            traceback.print_exc()

    async def connect_db(self) -> None:
        """Connect to the TimescaleDB database."""
        try:
            db_config = {
                'host': config.database.host,
                'port': config.database.port,
                'database': config.database.database,
                'user': config.database.user,
                'password': config.database.password
            }
            self.conn = await asyncpg.connect(**db_config)
        except Exception as e:
            self.show_error(f"Database connection failed: {e}")
            raise

    async def load_data(self) -> None:
        """Load latest 10 state records."""
        if not self.conn:
            self.show_error("No database connection")
            return

        if self.loading:
            return

        self.loading = True
        self.update_status("Loading...")

        # Show loading indicator
        container = self.query_one("#scroll-container", VerticalScroll)
        container.remove_children()
        loading = LoadingIndicator()
        await container.mount(loading)

        try:
            # Build and execute query for 10 latest states (as JSONB)
            query = """
            SELECT
                row_number() OVER (ORDER BY time DESC) as state_num,
                time::timestamp(0) as timestamp,
                state
            FROM state_logs
            ORDER BY time DESC
            LIMIT 10
            """

            rows = await self.conn.fetch(query)

            # Process and display the data
            await self.display_cards(rows)

            # Scroll to top after loading new content
            container.scroll_home()

            self.update_status(f"Loaded {len(self.state_data)} states")

        except Exception as e:
            self.show_error(f"Failed to load data: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.loading = False

    async def display_cards(self, rows: List[asyncpg.Record]) -> None:
        """Display state data as cards with trees."""

        # Clear existing content
        container = self.query_one("#scroll-container", VerticalScroll)
        container.remove_children()

        # Process rows
        self.state_data = []
        self.cards = []

        for row in rows:
            state_num = row['state_num']
            timestamp = str(row['timestamp'])
            state_json = row['state']  # This is already a Python dict from asyncpg

            # Ensure state_json is a dict
            if isinstance(state_json, str):
                try:
                    state_json = json.loads(state_json)
                except:
                    logger.error(f"Failed to parse state JSON: {state_json}")
                    state_json = {'error': 'Failed to parse state data'}
            elif not isinstance(state_json, dict):
                state_json = {'raw': str(state_json)}

            self.state_data.append({
                'num': state_num,
                'timestamp': timestamp,
                'state': state_json
            })

            # Create card with tree view
            card = StateCard(
                state_num=state_num,
                timestamp=timestamp,
                state_data=state_json
            )
            self.cards.append(card)
            await container.mount(card)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id

        if button_id == "refresh-btn" and not self.loading:
            asyncio.create_task(self.load_data())
        elif button_id == "export-btn":
            self.export_data()

    def export_data(self) -> None:
        """Export current state data to a file."""
        if not self.state_data:
            self.update_status("No data to export")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/tmp/state_logs_export_{timestamp}.json"

            # Convert data to JSON
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'states': self.state_data
            }

            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)

            self.update_status(f"Exported to {filename}")

        except Exception as e:
            self.show_error(f"Export failed: {e}")

    def update_status(self, message: str) -> None:
        """Update the status label."""
        self.status_text = message
        try:
            label = self.query_one("#status", Label)
            label.update(message)
        except:
            pass

    def show_error(self, message: str) -> None:
        """Display an error message."""
        self.last_error = message
        # Log to file for debugging
        logger.error(f"[StateLogsView] Error: {message}")
        self.update_status(f"Error: {message}")

    async def on_unmount(self) -> None:
        """Clean up when the widget is unmounted."""
        # Close database connection
        if self.conn:
            await self.conn.close()
            self.conn = None