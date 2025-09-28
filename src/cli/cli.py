from textual.app import App, ComposeResult
from textual.widgets import Header, Tab, TabPane, TabbedContent
from textual.binding import Binding
from pathlib import Path
from src.lighthouse import get_lighthouse, LighthouseConfig
from src.views.can_view import CANView
from src.views.meteo_view import MeteoView
from src.views.power_view import PowerView
from src.views.state_view import StateView
from src.views.health_view import HealthView
from src.views.state_logs_view import StateLogsView
from src.views.command_logs_view import CommandLogsView
import asyncio

class MonitoringCLI(App):
    """A CLI monitoring application using the LighthouseSystem."""

    BINDINGS = [
        Binding("ctrl+t", "toggle_theme", "Toggle theme", show=True),
        Binding("ctrl+h", "toggle_help", "Toggle help (this box)", show=True),
        Binding("ctrl+s", "screenshot", "Take Screenshot", show=True),
    ]

    CSS = """
    Screen {
        align: center middle;
    }

    TabbedContent {
        width: 100%;
        height: 1fr;
    }

    CANView, ProtoStateView, MeteoView, PowerView, StateView, HealthView, StateLogsView, CommandLogsView {
        width: 1fr;
        height: 1fr;
        padding: 1;
        overflow: auto;
    }
    """

    def __init__(self, lighthouse):
        super().__init__()
        self.lighthouse = lighthouse
        self.current_tab_index = 0
        self.tab_ids = ["can-tab", "c-state-tab", "meteo-tab", "power-tab", "health-tab",
                        "state-logs-tab", "cmd-logs-tab"]
        self.help_panel_visible = False

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()

        with TabbedContent(initial="can-tab"):
            with TabPane("CAN", id="can-tab"):
                yield CANView(self.lighthouse)
            with TabPane("Internal State", id="c-state-tab"):
                yield StateView(self.lighthouse)
            with TabPane("Meteo", id="meteo-tab"):
                yield MeteoView(self.lighthouse)
            with TabPane("Power", id="power-tab"):
                yield PowerView(self.lighthouse)
            with TabPane("Health", id="health-tab"):
                yield HealthView()
            with TabPane("State Logs", id="state-logs-tab"):
                yield StateLogsView()
            with TabPane("Cmd Logs", id="cmd-logs-tab"):
                yield CommandLogsView()

    async def on_mount(self) -> None:
        """Handle app mounting."""
        self.query_one(TabbedContent).focus()
        self.action_show_help_panel()

    async def action_toggle_theme(self) -> None:
        """Toggle between light and dark theme."""
        self.dark = not self.dark

    def action_toggle_help(self) -> None:
        """An action to toggle the help panel visibility."""
        self.help_panel_visible = not self.help_panel_visible
        if self.help_panel_visible:
            self.action_show_help_panel()
        else:
            self.action_hide_help_panel()

    async def on_unmount(self) -> None:
        """Clean up when the app is closing."""
        try:
            # Clean up all views systematically
            view_types = [
                CANView,
                StateView,
                MeteoView,
                PowerView,
                HealthView,
                StateLogsView,
                CommandLogsView
            ]

            for view_type in view_types:
                try:
                    view = self.query_one(view_type)
                    if hasattr(view, 'on_unmount'):
                        await view.on_unmount()
                except Exception as e:
                    if hasattr(self.lighthouse, 'logger'):
                        self.lighthouse.logger.error(f"Error cleaning up {view_type.__name__}: {e}")

            # Clean up lighthouse last
            if hasattr(self, 'lighthouse') and self.lighthouse:
                await self.lighthouse.stop()

        except Exception as e:
            if hasattr(self.lighthouse, 'logger'):
                self.lighthouse.logger.error(f"Error during unmount: {e}")

async def run_app():
    """Run the monitoring CLI application."""
    # Setup log directory in /tmp/
    log_dir = Path("/tmp/lighthouse/logs")
    # Create the directory if it doesn't exist
    log_dir.parent.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(exist_ok=True)

    # Initialize Lighthouse system
    config = LighthouseConfig(log_dir=str(log_dir))
    lighthouse = await get_lighthouse()
    await lighthouse.initialize(config=config)

    # Create and run the app with the initialized lighthouse
    app = MonitoringCLI(lighthouse)
    await app.run_async()

def cli():
    """Entry point for the CLI application."""
    try:
        asyncio.run(run_app())
    except Exception as e:
        print(f"Application error: {e}")
        raise

# Make the cli function available when importing this module
__all__ = ['cli']

if __name__ == "__main__":
    cli()
