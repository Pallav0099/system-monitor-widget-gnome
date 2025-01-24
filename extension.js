// move this file to "~/.local/share/gnome-shell/extensions/"
const { St } = imports.gi;
const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;
const GLib = imports.gi.GLib;

let systemMonitor;

class SystemMonitor extends PanelMenu.Button {
    _init() {
        super._init(0.0, "System Monitor", false);

        this.label = new St.Label({ text: "Loading..." });
        this.add_child(this.label);

        // Modify here and in metrics.py for altering how fast you want data to update
        this._updateMetrics();
        this._timer = GLib.timeout_add_seconds(0, 1, () => {
            this._updateMetrics();
            return true;
        });
    }

    _updateMetrics() {
        const filePath = "/tmp/system_metrics.json";
        try {
            const [ok, contents] = GLib.file_get_contents(filePath);
            if (ok) {
                let data = JSON.parse(contents);
                this.label.set_text(
                    `CPU: ${data.cpu}% | Mem: ${data.memory}% | Disk: ${data.disk}%`
                );
            }
        } catch (e) {
            this.label.set_text("Error: Unable to load metrics");
        }
    }

    destroy() {
        GLib.source_remove(this._timer);
        super.destroy();
    }
}

function init() {}

function enable() {
    systemMonitor = new SystemMonitor();
    Main.panel.addToStatusArea("system-monitor", systemMonitor);
}

function disable() {
    systemMonitor.destroy();
}

