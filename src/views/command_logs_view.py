"""Command logs view for displaying TimescaleDB command_logs table data."""

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
    filename='/tmp/panopticon_command_logs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CommandLogsView')


class CommandCard(Container):
    """A card widget for displaying a single command entry as a tree."""

    DEFAULT_CSS = """
    CommandCard {
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

    def __init__(self, cmd_num: int, timestamp: str, client_type: str, command_data: Dict[str, Any]) -> None:
        """Initialize a command card.

        Args:
            cmd_num: Command number
            timestamp: Timestamp string
            client_type: Client type string
            command_data: Nested command data dictionary
        """
        super().__init__()
        self.cmd_num = cmd_num
        self.timestamp = timestamp
        self.client_type = client_type
        self.command_data = command_data

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Static(f"════ COMMAND #{self.cmd_num} @ {self.timestamp} ════", classes="card-header")

        # Create tree for command data
        tree: Tree = Tree("Command")
        tree.root.expand()

        # Separate protocol header fields from payload
        header_keys = {'clientType', 'fromCvSubsystem', 'important', 'sessionId', 'protocolVersion'}
        header_data = {}
        payload_data = {}

        for key, value in self.command_data.items():
            if key in header_keys:
                header_data[key] = value
            else:
                payload_data[key] = value

        # Add payload first (more important)
        if payload_data:
            payload_node = tree.root.add("[cyan]Payload[/cyan]")
            payload_node.expand()
            for key in sorted(payload_data.keys()):
                self._add_node(payload_node, key, payload_data[key])
        else:
            tree.root.add("[dim italic](no payload)[/dim italic]")

        # Add protocol header (less important)
        if header_data:
            header_node = tree.root.add("[dim]Protocol Header[/dim]")
            # Keep collapsed by default - user can expand if needed
            for key in sorted(header_data.keys()):
                self._add_node(header_node, key, header_data[key], dim=True)

        yield tree

    def _add_node(self, parent: TreeNode, key: str, value: Any, indent: int = 0, dim: bool = False) -> None:
        """Recursively add nodes to the tree."""
        # Apply dimming if requested
        style_prefix = "[dim]" if dim else ""
        style_suffix = "[/dim]" if dim else ""

        if isinstance(value, dict):
            if not value:
                # Empty dict
                node = parent.add(f"{style_prefix}[cyan]{key}[/cyan]: (empty){style_suffix}")
            else:
                # Add expandable node for nested dict
                node = parent.add(f"{style_prefix}[cyan]{key}[/cyan]{style_suffix}")
                node.expand()  # Auto-expand first level
                # Recursively add children
                for k in sorted(value.keys()):
                    self._add_node(node, k, value[k], indent + 1, dim)
        elif isinstance(value, list):
            # Handle arrays
            node = parent.add(f"{style_prefix}[cyan]{key}[/cyan]: Array[{len(value)}]{style_suffix}")
            if value and indent < 3:  # Limit expansion depth
                node.expand()
                for i, item in enumerate(value):
                    self._add_node(node, f"[{i}]", item, indent + 1, dim)
        else:
            # Leaf node - display value
            if value is None:
                display_value = "null"
            elif isinstance(value, bool):
                display_value = f"[green]{str(value).lower()}[/green]"
            elif isinstance(value, (int, float)):
                display_value = f"[yellow]{value}[/yellow]"
            elif value == "(empty)":
                display_value = "(empty)"
            elif value == "(has fields)":
                display_value = "(has fields)"
            else:
                display_value = f"[white]{value}[/white]"

            parent.add(f"{style_prefix}[cyan]{key}[/cyan]: {display_value}{style_suffix}")


class CommandLogsView(Vertical):
    """Display command logs from TimescaleDB with manual refresh and export."""

    DEFAULT_CSS = """
    CommandLogsView {
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
        """Initialize the command logs view."""
        super().__init__()
        self.conn: Optional[asyncpg.Connection] = None
        self.last_error = None
        self.command_data = []  # Store fetched data
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
        """Load latest 10 command records."""
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
            # Build and execute query for 10 latest commands
            query = self.build_query()
            rows = await self.conn.fetch(query)

            # Process and display the data
            await self.display_cards(rows)

            # Scroll to top after loading new content
            container.scroll_home()

            self.update_status(f"Loaded {len(self.command_data)} commands")

        except Exception as e:
            self.show_error(f"Failed to load data: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.loading = False

    def build_query(self) -> str:
        """Build the SQL query for latest 10 commands."""
        return """
        WITH RECURSIVE commands AS (
          SELECT time, client_type, command, row_number() OVER (ORDER BY time DESC) as rn
          FROM command_logs
          WHERE command IS NOT NULL
          ORDER BY time DESC
          LIMIT 10
        ),
        flat(rn, time, client_type, path, value, type, level) AS (
          SELECT rn, time, client_type, key, value, jsonb_typeof(value), 0
          FROM commands, jsonb_each(command)
          UNION ALL
          SELECT f.rn, f.time, f.client_type, f.path||'.'||e.key, e.value, jsonb_typeof(e.value), f.level+1
          FROM flat f, jsonb_each(f.value) e
          WHERE f.type='object' AND f.level<10
        ),
        formatted AS (
          SELECT rn, time::timestamp(0) as timestamp, client_type, path,
                 CASE
                   WHEN type='object' AND value='{}' THEN '(empty)'
                   WHEN type='object' THEN '(has fields)'
                   WHEN type='array' THEN 'Array['||jsonb_array_length(value)||']'
                   ELSE value::text
                 END as value
          FROM flat
          WHERE type!='object' OR value='{}'
        )
        SELECT rn as cmd_num, timestamp, client_type, path as field, value
        FROM formatted
        ORDER BY rn, field
        """

    async def display_cards(self, rows: List[asyncpg.Record]) -> None:
        """Display command data as cards with trees."""

        # Clear existing content
        container = self.query_one("#scroll-container", VerticalScroll)
        container.remove_children()

        # Group rows by command number and build nested structure
        self.command_data = []
        commands_dict = {}  # cmd_num -> {timestamp, client_type, data}

        for row in rows:
            cmd_num = row['cmd_num']

            if cmd_num not in commands_dict:
                commands_dict[cmd_num] = {
                    'timestamp': str(row['timestamp']),
                    'client_type': row['client_type'] or "",
                    'data': {}
                }

            # Build nested structure from dotted paths
            field = row['field']
            value = row['value']

            if field and value:
                # Parse the dotted path into nested dictionary
                parts = field.split('.')
                current = commands_dict[cmd_num]['data']

                # Navigate to create nested structure
                for i, part in enumerate(parts[:-1]):
                    if part not in current:
                        current[part] = {}
                    elif not isinstance(current[part], dict):
                        # Convert to dict if needed
                        current[part] = {'_value': current[part]}
                    current = current[part]

                # Set the final value
                final_key = parts[-1]

                # Handle special cases
                if value == '(empty)':
                    current[final_key] = {}
                elif value == '(has fields)':
                    if final_key not in current:
                        current[final_key] = {}
                elif value.startswith('Array['):
                    # Extract array size
                    try:
                        size = int(value[6:-1])
                        current[final_key] = f"Array[{size}]"
                    except:
                        current[final_key] = value
                else:
                    # Clean up value (remove quotes if present)
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    current[final_key] = value

        # Convert to list format
        for cmd_num in sorted(commands_dict.keys()):
            cmd_info = commands_dict[cmd_num]
            self.command_data.append({
                'num': cmd_num,
                'timestamp': cmd_info['timestamp'],
                'client_type': cmd_info['client_type'],
                'data': cmd_info['data']
            })

        # Create and mount cards
        self.cards = []
        for cmd in self.command_data:
            card = CommandCard(
                cmd_num=cmd['num'],
                timestamp=cmd['timestamp'],
                client_type=cmd['client_type'],
                command_data=cmd['data']
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
        """Export current command data to a file."""
        if not self.command_data:
            self.update_status("No data to export")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"/tmp/command_logs_export_{timestamp}.json"

            # Convert data to JSON
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'commands': self.command_data
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
        logger.error(f"[CommandLogsView] Error: {message}")
        self.update_status(f"Error: {message}")

    async def on_unmount(self) -> None:
        """Clean up when the widget is unmounted."""
        # Close database connection
        if self.conn:
            await self.conn.close()
            self.conn = None