# System Monitor Widget for GNOME

A lightweight and customizable system monitor widget for GNOME that displays CPU and memory usage in real-time, along with draggable graphs. Perfect for monitoring system performance directly on your desktop!

## Features
- Real-time CPU and memory usage graphs.
- Drag-and-drop functionality for repositioning the widget.
- Auto-start support using systemd.
- Lightweight and user-friendly interface.
- Compatible with GNOME desktop environments.

## Prerequisites
- **Python 3.6+**
- **GNOME Desktop Environment**
- Required Python libraries:
  - `psutil`
  - `PyGObject`

# If you don't have these installed simply run these commands
  sudo apt update
  sudo apt install python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0
  pip install psutil
  
## Installation
1. Clone this repository:
   git clone https://github.com/Pallav0099/system-monitor-widget-gnome.git
   cd system-monitor-widget-gnome

#skip the next step if you already have the dependencies installed.
2. pip install -r dependencies.txt

3. (OPTIONAL) Setup the widget to auto start using systemd.
   - Copy the system-monitor.service file to the systemd user directory:
     mkdir -p ~/.config/systemd/user/
     cp system-monitor.service ~/.config/systemd/user/
   
   - Reload The systemd daemon:
     systemctl --user daemon-reload

   - Enable and Start the service:
     systemctl --user enable system-monitor.service
     systemctl --user start system-monitor.service
   
4. Run the widget manually:
   python3 system_monitor_widget.py

5. Usage
- Launch the widget, and it will appear on your desktop.
- Drag the widget to reposition it by clicking and holding anywhere on the window.
- Close the widget by clicking the window's close button.

6. Troubleshooting
### Issue: Service doesn't start
- Check the service logs:
  journalctl --user -u system-monitor.service
  
### Issue: Missing python dependencies
- Reinstall dependencies:
  pip install -r dependencies.txt
  
### **Contributing**
Encourage others to contribute to this project.
  



   


   





