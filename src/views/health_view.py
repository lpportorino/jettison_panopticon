from time import strftime, localtime
from textual.widgets import Switch, Label, RichLog
from textual.containers import Horizontal, Vertical
from textual.app import ComposeResult
from textual import on
from textual.reactive import reactive
from typing import Dict, Optional
from rich.table import Table
from rich.text import Text
from src.health_monitor import get_health_monitor, HealthMonitor, HealthMetric

class HealthView(Vertical):
    """Health monitoring view for displaying service health metrics using RichLog."""

    DEFAULT_CSS = """
    HealthView {
        height: 100%;
        width: 100%;
    }

    #controls {
        dock: top;
        height: 3;
        padding: 1;
        background: $panel;
        border-bottom: solid $primary;
    }

    Switch {
        dock: bottom;
        background: $boost;
        margin: 1 0;
    }

    Label {
        dock: bottom;
        padding: 0 1;
    }

    #status-bar {
        dock: bottom;
        height: 3;
        padding: 1;
        background: $panel;
        border-top: solid $primary;
    }

    RichLog {
        height: 100%;
        border: solid $primary;
        background: $surface;
        color: $text;
        padding: 0 1;
        scrollbar-gutter: stable;
        overflow-y: scroll;
    }
    """

    current_metrics = reactive({})
    paused = reactive(False)

    def __init__(self):
        super().__init__()
        self._monitor: Optional[HealthMonitor] = None
        self._log: Optional[RichLog] = None
        self._status_bar: Optional[Label] = None
        self._last_scroll_position: Optional[float] = None

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        with Horizontal(id="controls"):
            yield Label("Health Monitor Control")
            yield Switch(value=False, id="pause")

        # Initialize RichLog with auto_scroll disabled and minimum width set to 1
        self._log = RichLog(
            highlight=True,
            markup=True,
            wrap=True,
            auto_scroll=False,  # Disable auto-scrolling
            min_width=1  # Set minimum width to 1 instead of None
        )
        yield self._log

        with Horizontal(id="status-bar"):
            self._status_bar = Label("Initializing...")
            yield self._status_bar

    @staticmethod
    def create_metrics_table(metrics: Dict[str, HealthMetric]) -> Table:
        """Create a Rich table for the metrics."""
        table = Table(
            "Service",
            "Metric",
            "Health",
            "Cap",
            "Percentage",
            "Status",
            title=f"Health Status - {strftime('%H:%M:%S', localtime())}",
            title_style="bold blue",
            border_style="blue",
            expand=True,  # Make table use full width
            padding=(0, 1),  # Reduce padding to save space
        )

        for service_id, metric in sorted(metrics.items()):
            status_style = {
                "Healthy": "bold green",
                "Warning": "bold yellow",
                "Critical": "bold red"
            }.get(metric.status, "white")

            table.add_row(
                metric.service_path,
                metric.metric_type,
                str(metric.health),
                str(metric.cap),
                f"{metric.health_percentage:.1f}%",
                Text(metric.status, style=status_style)
            )

        return table

    def _save_scroll_position(self) -> None:
        """Save the current scroll position."""
        if self._log and self._log.scroll_offset is not None:
            self._last_scroll_position = self._log.scroll_offset.y

    def _restore_scroll_position(self) -> None:
        """Restore the previously saved scroll position."""
        if self._log and self._last_scroll_position is not None:
            self._log.scroll_to(0, self._last_scroll_position, animate=False)

    async def on_mount(self) -> None:
        """Handle component mounting with monitor initialization."""
        self._monitor = await get_health_monitor()
        if self._monitor:
            self._monitor.set_health_callback(self.handle_health_update)

    def on_unmount(self) -> None:
        """Handle component unmounting."""
        if self._monitor:
            self._monitor.clear_health_callback()
            self._monitor = None

    def handle_health_update(self, metrics: Dict[str, HealthMetric]) -> None:
        """Handle health metric updates."""
        if self.paused or not self._log:
            return

        try:
            # Save current scroll position
            self._save_scroll_position()

            # Store current metrics
            old_metrics = self.current_metrics
            self.current_metrics = metrics

            # Create and display the metrics table
            table = self.create_metrics_table(metrics)
            self._log.clear()
            self._log.write(table)

            # Log changes
            changes = []
            for service_id, new_metric in metrics.items():
                old_metric = old_metrics.get(service_id)
                if old_metric and old_metric != new_metric:
                    status_style = {
                        "Healthy": "bold green",
                        "Warning": "bold yellow",
                        "Critical": "bold red"
                    }.get(new_metric.status, "white")

                    changes.append(
                        f"[blue]{service_id}[/blue]: "
                        f"{old_metric.health}/{old_metric.cap} ({old_metric.status}) → "
                        f"{new_metric.health}/{new_metric.cap} ([{status_style}]{new_metric.status}[/{status_style}])"
                    )

            if changes:
                self._log.write("\n[bold]Recent Changes:[/bold]")
                for change in changes:
                    self._log.write(change)

            # Restore scroll position after update
            self._restore_scroll_position()

            self.update_status_bar()

        except Exception as e:
            self._status_bar.update(f"Error updating health data: {str(e)}")

    def update_status_bar(self) -> None:
        """Update the status bar with summary information."""
        if not self._status_bar:
            return

        total = len(self.current_metrics)
        healthy = sum(1 for m in self.current_metrics.values() if m.status == "Healthy")
        warning = sum(1 for m in self.current_metrics.values() if m.status == "Warning")
        critical = sum(1 for m in self.current_metrics.values() if m.status == "Critical")

        status_text = (
            f"Total Services: {total} | "
            f"Healthy: {healthy} | "
            f"Warning: {warning} | "
            f"Critical: {critical} | "
            f"Last Update: {strftime('%H:%M:%S', localtime())}"
        )
        self._status_bar.update(status_text)

    @on(Switch.Changed, "#pause")
    def handle_pause_change(self, event: Switch.Changed) -> None:
        """Handle changes to the pause switch."""
        self.paused = event.value
