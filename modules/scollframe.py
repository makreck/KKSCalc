import platform
import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, scrollbar_width=14, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview, width=scrollbar_width)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.inner = tk.Frame(self.canvas)
        self.inner_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.inner.bind("<Enter>", self.on_bind_wheel_action)
        self.inner.bind("<Leave>", self.on_unbind_wheel_action)

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.inner_id, width=event.width)

    def on_mousewheel(self, event, scroll=None):
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
        elif platform.system() == "Linux":
            self.canvas.yview_scroll(int(scroll), "units")
        else:
            self.canvas.yview_scroll(int(-event.delta), "units")

    def on_bind_wheel_action(self, event):
        if platform.system() == "Linux":
            self.bind_all("<Button-4>", lambda event: self.on_mousewheel(event, scroll=-1))
            self.bind_all("<Button-5>", lambda event: self.on_mousewheel(event, scroll=1))
        else:
            self.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_unbind_wheel_action(self, event):
        if platform.system() == "Linux":
            self.unbind_all("<Button-4>")
            self.unbind_all("<Button-5>")
        else:
            self.unbind_all("<MouseWheel>")

    def get(self) -> tk.Widget:
        return self.inner
