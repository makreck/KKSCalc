import tkinter as tk

class ToolTip:
    def __init__(self, root, widget, text, wait_time=500, showtime=2500):
        self.root      = root
        self.widget    = widget
        self.text      = text
        self.wait_time = wait_time
        self.showtime  = showtime
        self.popup     = None
        self.label     = None
        self.wait_id   = 0
        self.timer_id  = 0
        self.widget.bind("<Enter>", self.prepare_tip)
        self.widget.bind("<Leave>", self.hide_tip)
        self.widget.bind("<ButtonRelease-1>", self.hide_tip)

    def prepare_tip(self, event=None):
        self.wait_id = self.widget.after(self.wait_time, self.show_tip)
        
    def show_tip(self, event=None):
        if self.popup: return

        self.popup = tk.Toplevel(self.root, background="yellow")
        self.popup.overrideredirect(True)
        self.label = tk.Label(self.popup, text=self.text, background="yellow", relief="flat", borderwidth=4)
        self.label.pack(fill="both", padx=4, pady=4)
        
        x = self.widget.winfo_rootx() + 16
        y = self.widget.winfo_rooty() + 48
        w = self.label.winfo_reqwidth() + 8
        h = self.label.winfo_reqheight()

        self.popup.geometry(f"{w}x{h}+{x}+{y}")
        self.root.update_idletasks()
        self.timer_id = self.popup.after(self.showtime, self.hide_tip)

    def hide_tip(self, event=None):
        try:
            if self.wait_id:
                self.widget.after_cancel(self.wait_id)
            if self.timer_id:
                self.popup.after_cancel(self.timer_id)
            if self.label:
                self.label.destroy()
            if self.popup:
                self.popup.destroy()
        finally:
            self.popup    = None
            self.label    = None
            self.timer_id = None
            self.root.update_idletasks()
