import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from metrics import get_cpu_usage, get_memory_usage, get_disk_usage

class TransparentWindow(Gtk.Window):
    def __init__(self):
        super().__init__()

        self.set_decorated(False)
        print("Window decorations removed.")

        # Set window transparent
        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
            print("Transparency enabled.")
        else:
            print("Transparency not supported. Ensure compositing is enabled in your desktop environment.")

        self.overlay = Gtk.Overlay()
        self.add(self.overlay)

        # Transparent background code
        self.background = Gtk.DrawingArea()
        self.background.connect("draw", self.on_draw_background)
        self.overlay.add(self.background)

        self.system_monitor = SystemMonitorWidget()
        self.overlay.add_overlay(self.system_monitor)

        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("button-press-event", self.on_button_press)
        self.connect("key-press-event", self.on_key_press)
        print("Window interaction disabled.")

        self.set_size_request(400, 600)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def on_draw_background(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)  # Fully transparent background
        cr.paint()

    def on_button_press(self, widget, event):
        print("Button press event blocked.")
        return True

    def on_key_press(self, widget, event):
        print("Key press event blocked.")
        return True

class SystemMonitorWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Data for graphs
        self.cpu_usage = []
        self.memory_usage = []
        self.disk_usage = []

        # CPU Graph
        self.cpu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.cpu_label = Gtk.Label(label="CPU Usage")
        self.drawing_area_cpu = Gtk.DrawingArea()
        self.drawing_area_cpu.set_name("cpu-drawing-area")
        self.drawing_area_cpu.connect("draw", self.on_draw_cpu)
        self.cpu_box.pack_start(self.cpu_label, False, False, 0)
        self.cpu_box.pack_start(self.drawing_area_cpu, True, True, 0)

        # Memory Graph
        self.memory_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.memory_label = Gtk.Label(label="Memory Usage")
        self.drawing_area_memory = Gtk.DrawingArea()
        self.drawing_area_memory.set_name("memory-drawing-area")
        self.drawing_area_memory.connect("draw", self.on_draw_memory)
        self.memory_box.pack_start(self.memory_label, False, False, 0)
        self.memory_box.pack_start(self.drawing_area_memory, True, True, 0)

        # Disk Usage
        self.disk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.disk_label = Gtk.Label(label="Disk Usage")
        self.drawing_area_disk = Gtk.DrawingArea()
        self.drawing_area_disk.set_name("disk-drawing-area")
        self.drawing_area_disk.connect("draw", self.on_draw_disk)
        self.disk_box.pack_start(self.disk_label, False, False, 0)
        self.disk_box.pack_start(self.drawing_area_disk, True, True, 0)

        self.pack_start(self.cpu_box, True, True, 0)
        self.pack_start(self.memory_box, True, True, 0)
        self.pack_start(self.disk_box, True, True, 0)

        # Data update timer
        GLib.timeout_add(1000, self.update_data)

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

        self.drawing_area_cpu.queue_draw()
        self.drawing_area_memory.queue_draw()
        self.drawing_area_disk.queue_draw()

        return True

    def on_draw_cpu(self, widget, cr):
        """Draw the CPU usage graph."""
        self.draw_graph(widget, cr, self.cpu_usage, (255/255, 239/255, 213/255)) 

    def on_draw_memory(self, widget, cr):
        """Draw the Memory usage graph."""
        self.draw_graph(widget, cr, self.memory_usage, (240/255, 248/255, 255/255)) 

    def on_draw_disk(self, widget, cr):
        """Draw the Disk usage graph."""
        self.draw_graph(widget, cr, self.disk_usage, (240/255, 255/255, 240/255)) 

    def draw_graph(self, widget, cr, data, color):
        """Generic function to draw a graph."""
        width, height = widget.get_allocated_width(), widget.get_allocated_height()

        # Set graph background to white
        cr.set_source_rgba(0, 0, 0, 0) 
        cr.rectangle(0, 0, width, height)
        cr.fill()

        # Draw the graph border
        cr.set_source_rgb(0, 0, 0)  # Black border
        cr.set_line_width(2)
        cr.rectangle(0, 0, width, height)
        cr.stroke()

        # Draw the graph data
        cr.set_source_rgb(*color)  # Use the provided color
        cr.set_line_width(2)
        for i in range(1, len(data)):
            cr.move_to((i - 1) * (width / 50), height - (data[i - 1] / 100 * height))
            cr.line_to(i * (width / 50), height - (data[i] / 100 * height))
            cr.stroke()

if __name__ == "__main__":
    win = TransparentWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    #update
