import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from metrics import get_cpu_usage, get_memory_usage

class SystemMonitorWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="System Monitor")
        self.set_default_size(400, 300)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Apply CSS styles
        self.apply_styles()

        # Initialize data for graphs
        self.cpu_usage = []
        self.memory_usage = []

        # Create a drawing area for the graph
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_name("drawing-area")  # Assign a CSS name
        self.drawing_area.connect("draw", self.on_draw)
        self.add(self.drawing_area)

        # Set up drag handling for repositioning
        self.connect("button-press-event", self.on_button_press)
        self.connect("motion-notify-event", self.on_mouse_move)
        self.connect("button-release-event", self.on_button_release)

        # Variables for dragging
        self.dragging = False
        self.prev_x = 0
        self.prev_y = 0

        # Start a timer to update the graph every second
        GLib.timeout_add(1000, self.update_data)

    def apply_styles(self):
        """Load and apply CSS styles from the styles.css file."""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")

        # Apply the CSS to the default screen
        screen = Gdk.Screen.get_default()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_data(self):
        """Fetch new data for CPU and memory usage and update the graph."""
        self.cpu_usage.append(get_cpu_usage())
        self.memory_usage.append(get_memory_usage())

        if len(self.cpu_usage) > 50:
            self.cpu_usage.pop(0)
        if len(self.memory_usage) > 50:
            self.memory_usage.pop(0)

        self.drawing_area.queue_draw()  # Trigger redraw
        return True

    def on_draw(self, widget, cr):
        """Draw CPU and memory usage graphs on the drawing area."""
        width, height = widget.get_allocated_width(), widget.get_allocated_height()
        cr.set_source_rgb(1, 1, 1)  # White background
        cr.paint()

        # Draw CPU graph (Blue)
        cr.set_source_rgb(0, 0, 1)
        for i in range(1, len(self.cpu_usage)):
            cr.move_to(i * (width / 50), height - (self.cpu_usage[i-1] / 100 * height))
            cr.line_to((i+1) * (width / 50), height - (self.cpu_usage[i] / 100 * height))
            cr.stroke()

        # Draw Memory graph (Green)
        cr.set_source_rgb(0, 1, 0)
        for i in range(1, len(self.memory_usage)):
            cr.move_to(i * (width / 50), height - (self.memory_usage[i-1] / 100 * height))
            cr.line_to((i+1) * (width / 50), height - (self.memory_usage[i] / 100 * height))
            cr.stroke()

    def on_button_press(self, widget, event):
        """Start dragging the window."""
        self.dragging = True
        self.prev_x, self.prev_y = event.x, event.y

    def on_mouse_move(self, widget, event):
        """Handle window dragging while the mouse moves."""
        if self.dragging:
            dx = event.x - self.prev_x
            dy = event.y - self.prev_y
            x, y = self.get_position()
            self.move(x + dx, y + dy)
            self.prev_x, self.prev_y = event.x, event.y

    def on_button_release(self, widget, event):
        """Stop dragging the window."""
        self.dragging = False

if __name__ == "__main__":
    win = SystemMonitorWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
