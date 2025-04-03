import gi
gi.require_version('Gtk', '3.0')
import sys
from gi.repository import Gtk, Gdk, GLib
from metrics import get_cpu_usage, get_memory_usage, get_disk_usage

class TransparentWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        
        self.set_decorated(False)
        print("Window decorations removed.")
        
        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
            print("Transparency enabled.")
        else:
            print("Transparency not supported. Enable compositing in your desktop environment.")

        # Create overlay to stack widgets
        self.overlay = Gtk.Overlay()
        self.add(self.overlay)

        # Background layer
        self.background = Gtk.DrawingArea()
        self.background.connect("draw", self.draw_transparent_background)
        self.overlay.add(self.background)

        # Add system monitor widget
        self.system_monitor = SystemMonitorWidget()
        self.overlay.add_overlay(self.system_monitor)

        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK | Gdk.EventMask.POINTER_MOTION_MASK | Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("button-press-event", self.block_event)
        self.connect("key-press-event", self.block_event)
        print("Window interaction disabled.")

        # Set window size
        self.set_size_request(400, 600)
        self.connect("delete-event", Gtk.main_quit)

        # When the window is realized, position it to the right and vertically centered.
        self.connect("realize", self.on_realize)

        self.show_all()

    def draw_transparent_background(self, widget, cr):
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()
    
    def block_event(self, widget, event):
        print("Interaction blocked.")
        return True

    def on_realize(self, widget):
    
        screen = widget.get_screen()
        # Primary monitor index. O if NA
        monitor_index = screen.get_primary_monitor() if hasattr(screen, "get_primary_monitor") else 0
        monitor_geometry = screen.get_monitor_geometry(monitor_index)
        
        window_width, window_height = self.get_size()
        # x: right side of the monitor (monitor's x + monitor's width) minus the window width.
        # y: monitor's y plus half the difference between monitor height and window height (vertically centered).
        new_x = monitor_geometry.x + monitor_geometry.width - window_width
        new_y = monitor_geometry.y + (monitor_geometry.height - window_height) // 2
        
        self.move(new_x, new_y)
        print(f"Window moved to: ({new_x}, {new_y})")

class SystemMonitorWidget(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        # Data Point storage
        self.cpu_usage = []
        self.memory_usage = []
        self.disk_usage = []

        # Sections
        self.cpu_box = self.create_graph_section("CPU Usage", self.draw_cpu_graph)
        self.memory_box = self.create_graph_section("Memory Usage", self.draw_memory_graph)
        self.disk_box = self.create_graph_section("Disk Usage", self.draw_disk_graph)

        self.pack_start(self.cpu_box, True, True, 0)
        self.pack_start(self.memory_box, True, True, 0)
        self.pack_start(self.disk_box, True, True, 0)

        # Timeout update
        GLib.timeout_add(1000, self.update_data)

    def create_graph_section(self, label_text, draw_function):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        label = Gtk.Label(label=label_text)
        drawing_area = Gtk.DrawingArea()
        drawing_area.connect("draw", draw_function)
        box.pack_start(label, False, False, 0)
        box.pack_start(drawing_area, True, True, 0)
        return box

    def update_data(self):
        # Fetch new usage data and refresh the graph
        self.cpu_usage.append(get_cpu_usage())
        self.memory_usage.append(get_memory_usage())
        self.disk_usage.append(get_disk_usage())

        # Limit to 50 entries
        self.cpu_usage = self.cpu_usage[-50:]
        self.memory_usage = self.memory_usage[-50:]
        self.disk_usage = self.disk_usage[-50:]

        # Redraw graphs
        self.cpu_box.get_children()[1].queue_draw()
        self.memory_box.get_children()[1].queue_draw()
        self.disk_box.get_children()[1].queue_draw()
        
        return True

    def draw_cpu_graph(self, widget, cr):
        self.draw_graph(widget, cr, self.cpu_usage, (1, 0.94, 0.83))
    
    def draw_memory_graph(self, widget, cr):
        self.draw_graph(widget, cr, self.memory_usage, (0.94, 0.97, 1))
    
    def draw_disk_graph(self, widget, cr):
        self.draw_graph(widget, cr, self.disk_usage, (0.94, 1, 0.94))

    def draw_graph(self, widget, cr, data, color):
        width, height = widget.get_allocated_width(), widget.get_allocated_height()
        if width == 0 or height == 0:
            return

        # Clear background
        cr.set_source_rgba(0, 0, 0, 0)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        # Draw border
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(2)
        cr.rectangle(0, 0, width, height)
        cr.stroke()

        # Draw usage graph
        if data:
            cr.set_source_rgb(*color)
            cr.set_line_width(2)
            scale_x = width / 50
            scale_y = height / 100
            cr.move_to(0, height - data[0] * scale_y)
            for i in range(1, len(data)):
                cr.line_to(i * scale_x, height - data[i] * scale_y)
            cr.stroke()

if __name__ == "__main__":
    try:
        win = TransparentWindow()
        win.connect("destroy", Gtk.main_quit)
        Gtk.main()
    except Exception as e:
        print("Error:", e)
        sys.exit(1)

