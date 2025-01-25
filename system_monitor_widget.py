import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from metrics import get_cpu_usage, get_memory_usage, get_disk_usage

class SystemMonitorWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="System Monitor")
        self.set_default_size(300, 400)

        # Get screen dimensions using Gdk.Display and Gdk.Monitor
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor()
        geometry = monitor.get_geometry()
        screen_width = geometry.width
        screen_height = geometry.height

        window_width, window_height = self.get_default_size()
        self.move(0, (screen_height - window_height) // 2)

        # Apply CSS styles
        self.apply_styles()

        # Initialize data for graphs
        self.cpu_usage = []
        self.memory_usage = []
        self.disk_usage = []

        # Create a Box to organize the content vertically
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        # CPU Graph Section
        self.cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.cpu_label = Gtk.Label(label="CPU Usage")
        self.drawing_area_cpu = Gtk.DrawingArea()
        self.drawing_area_cpu.set_name("cpu-drawing-area")
        self.drawing_area_cpu.connect("draw", self.on_draw_cpu)
        self.cpu_box.pack_start(self.cpu_label, False, False, 0)
        self.cpu_box.pack_start(self.drawing_area_cpu, True, True, 0)

        # Memory Graph Section
        self.memory_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.memory_label = Gtk.Label(label="Memory Usage")
        self.drawing_area_memory = Gtk.DrawingArea()
        self.drawing_area_memory.set_name("memory-drawing-area")
        self.drawing_area_memory.connect("draw", self.on_draw_memory)
        self.memory_box.pack_start(self.memory_label, False, False, 0)
        self.memory_box.pack_start(self.drawing_area_memory, True, True, 0)

        # Disk Usage Section
        self.disk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.disk_label = Gtk.Label(label="Disk Usage")
        self.drawing_area_disk = Gtk.DrawingArea()
        self.drawing_area_disk.set_name("disk-drawing-area")
        self.drawing_area_disk.connect("draw", self.on_draw_disk)
        self.disk_box.pack_start(self.disk_label, False, False, 0)
        self.disk_box.pack_start(self.drawing_area_disk, True, True, 0)

        # Add all sections to the main Box
        self.box.pack_start(self.cpu_box, True, True, 0)
        self.box.pack_start(self.memory_box, True, True, 0)
        self.box.pack_start(self.disk_box, True, True, 0)

        # Start a timer to update the graph every second
        GLib.timeout_add(1000, self.update_data)

    def apply_styles(self):
        """Load and apply CSS styles from the styles.css file."""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("styles.css")
        display = Gdk.Display.get_default()
        screen = display.get_default_screen()
        style_context = Gtk.StyleContext()
        style_context.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def update_data(self):
        """Fetch new data for CPU, memory, and disk usage."""
        cpu = get_cpu_usage()
        memory = get_memory_usage()
        disk = get_disk_usage()

        self.cpu_usage.append(cpu)
        self.memory_usage.append(memory)
        self.disk_usage.append(disk)

        if len(self.cpu_usage) > 50:
            self.cpu_usage.pop(0)
        if len(self.memory_usage) > 50:
            self.memory_usage.pop(0)
        if len(self.disk_usage) > 50:
            self.disk_usage.pop(0)

        self.drawing_area_cpu.queue_draw()  # Trigger redraw for CPU graph
        self.drawing_area_memory.queue_draw()  # Trigger redraw for Memory graph
        self.drawing_area_disk.queue_draw()  # Trigger redraw for Disk graph

        return True

    def on_draw_cpu(self, widget, cr):
        """Draw the CPU usage graph."""
        self.draw_graph(widget, cr, self.cpu_usage, (0, 0, 1))  # Blue for CPU

    def on_draw_memory(self, widget, cr):
        """Draw the Memory usage graph."""
        self.draw_graph(widget, cr, self.memory_usage, (0, 1, 0))  # Green for Memory

    def on_draw_disk(self, widget, cr):
        """Draw the Disk usage graph."""
        self.draw_graph(widget, cr, self.disk_usage, (1, 0, 0))  # Red for Disk

    def draw_graph(self, widget, cr, data, color):
        """Generic function to draw a graph."""
        width, height = widget.get_allocated_width(), widget.get_allocated_height()
        cr.set_source_rgb(1, 1, 1)  # White background
        cr.paint()

        # Draw the graph border
        cr.set_source_rgb(0, 0, 0)  # Black border
        cr.set_line_width(2)
        cr.rectangle(0, 0, width, height)
        cr.stroke()

        # Draw the graph data
        cr.set_source_rgb(*color)
        for i in range(1, len(data)):
            cr.move_to((i - 1) * (width / 50), height - (data[i - 1] / 100 * height))
            cr.line_to(i * (width / 50), height - (data[i] / 100 * height))
            cr.stroke()

if __name__ == "__main__":
    win = SystemMonitorWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()