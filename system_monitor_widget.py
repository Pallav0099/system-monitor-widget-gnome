import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from metrics import get_cpu_usage, get_memory_usage

class SystemMonitorWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="System Monitor")
        self.set_default_size(300, 400)

        # Get screen dimensions
        screen_width = Gdk.Screen.get_default().get_width()
        screen_height = Gdk.Screen.get_default().get_height()
        window_width, window_height = self.get_default_size()
        self.move(0, (screen_height - window_height) // 2)

        # Apply CSS styles
        self.apply_styles()

        # Initialize data for graphs
        self.cpu_usage = []
        self.memory_usage = []

        # Create a Box to organize the content vertically
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # CPU Graph Section
        self.cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.cpu_label = Gtk.Label(label="CPU")
        self.drawing_area_cpu = Gtk.DrawingArea()
        self.drawing_area_cpu.set_name("cpu-drawing-area")
        self.drawing_area_cpu.connect("draw", self.on_draw_cpu)
        self.cpu_box.pack_start(self.cpu_label, False, False, 0)
        self.cpu_box.pack_start(self.drawing_area_cpu, True, True, 0)

        # Memory Graph Section
        self.memory_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.memory_label = Gtk.Label(label="Memory")
        self.drawing_area_memory = Gtk.DrawingArea()
        self.drawing_area_memory.set_name("memory-drawing-area")
        self.drawing_area_memory.connect("draw", self.on_draw_memory)
        self.memory_box.pack_start(self.memory_label, False, False, 0)
        self.memory_box.pack_start(self.drawing_area_memory, True, True, 0)

        # Add both sections to the main Box
        self.box.pack_start(self.cpu_box, True, True, 0)
        self.box.pack_start(self.memory_box, True, True, 0)

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

        self.drawing_area_cpu.queue_draw()  # Trigger redraw for CPU graph
        self.drawing_area_memory.queue_draw()  # Trigger redraw for Memory graph
        return True

    def on_draw_cpu(self, widget, cr):
        """Draw the CPU usage graph with a rectangle around it."""
        width, height = widget.get_allocated_width(), widget.get_allocated_height()
        cr.set_source_rgb(1, 1, 1)  # White background
        cr.paint()

        # Draw a rectangle around the CPU graph
        cr.set_source_rgb(0, 0, 0)  # Black border
        cr.set_line_width(2)
        cr.rectangle(0, 0, width, height)
        cr.stroke()

        # Draw CPU usage graph (Blue)
        cr.set_source_rgb(0, 0, 1)
        for i in range(1, len(self.cpu_usage)):
            cr.move_to(i * (width / 50), height - (self.cpu_usage[i-1] / 100 * height))
            cr.line_to((i+1) * (width / 50), height - (self.cpu_usage[i] / 100 * height))
            cr.stroke()

    def on_draw_memory(self, widget, cr):
        """Draw the Memory usage graph with a rectangle around it."""
        width, height = widget.get_allocated_width(), widget.get_allocated_height()
        cr.set_source_rgb(1, 1, 1)  # White background
        cr.paint()

        # Draw a rectangle around the Memory graph
        cr.set_source_rgb(0, 0, 0)  # Black border
        cr.set_line_width(2)
        cr.rectangle(0, 0, width, height)
        cr.stroke()

        # Draw Memory usage graph (Green)
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

