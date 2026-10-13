import ctypes
import math
import queue
import time
import tkinter as tk
from pynput import keyboard, mouse

# Artiixs Bounce — Windows overlay prototype
# Press Esc to exit.

events = queue.Queue()
mouse_position = [300, 300]
stop_event = queue.Queue()

TRANSPARENT_COLOR = "#ff00ff"
TEXT_COLOR = (101, 232, 255)  # cyan


def on_move(x, y):
    mouse_position[0] = x
    mouse_position[1] = y


def on_press(key):
    if key == keyboard.Key.esc:
        events.put(("__QUIT__", *mouse_position, time.monotonic()))
        return

    try:
        char = key.char
    except AttributeError:
        return

    if char and char.isprintable():
        events.put((char, *mouse_position, time.monotonic()))


def blend_to_transparent_color(rgb, amount):
    """Blend text color toward the transparent key color, creating a fade effect."""
    target = (255, 0, 255)
    return tuple(
        max(0, min(255, round(rgb[i] * (1.0 - amount) + target[i] * amount)))
        for i in range(3)
    )


def rgb_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


class ArtiixsBounce:
    def __init__(self, root):
        self.root = root
        self.items = []
        self.closing = False

        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.configure(bg=TRANSPARENT_COLOR)
        root.wm_attributes("-transparentcolor", TRANSPARENT_COLOR)

        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.geometry(f"{width}x{height}+0+0")

        self.canvas = tk.Canvas(
            root, bg=TRANSPARENT_COLOR, highlightthickness=0, bd=0
        )
        self.canvas.pack(fill="both", expand=True)

        # Make overlay click-through and keep it out of Alt+Tab.
        self.make_click_through()
        root.after(16, self.animate)

    def make_click_through(self):
        try:
            hwnd = self.root.winfo_id()
            user32 = ctypes.windll.user32
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            WS_EX_TOOLWINDOW = 0x00000080
            get_style = user32.GetWindowLongW
            set_style = user32.SetWindowLongW
            style = get_style(hwnd, GWL_EXSTYLE)
            set_style(hwnd, GWL_EXSTYLE,
                      style | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOOLWINDOW)
        except Exception:
            # The animation can still run if this Windows-specific tweak fails.
            pass

    def animate(self):
        if self.closing:
            return

        try:
            while True:
                char, x, y, started = events.get_nowait()
                if char == "__QUIT__":
                    self.close()
                    return
                self.items.append({
                    "char": char,
                    "start": started,
                })
        except queue.Empty:
            pass

        now = time.monotonic()
        alive = []
        self.canvas.delete("all")

        # Every active character follows the current pointer while bouncing.
        x, y = mouse_position
        duration = 1.2

        for item in self.items:
            elapsed = now - item["start"]
            if elapsed >= duration:
                continue

            progress = elapsed / duration
            jump = math.sin(progress * math.pi) * 42
            fade = min(1.0, max(0.0, progress))
            color = rgb_hex(blend_to_transparent_color(TEXT_COLOR, fade))

            self.canvas.create_text(
                int(x),
                int(y - 62 - jump),
                text=item["char"],
                font=("Segoe UI", 28, "bold"),
                fill=color,
                anchor="center",
            )
            alive.append(item)

        self.items = alive
        self.root.after(16, self.animate)

    def close(self):
        if self.closing:
            return
        self.closing = True
        try:
            self.root.destroy()
        except tk.TclError:
            pass


def main():
    root = tk.Tk()
    app = ArtiixsBounce(root)

    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_move=on_move)
    keyboard_listener.start()
    mouse_listener.start()

    try:
        root.mainloop()
    finally:
        keyboard_listener.stop()
        mouse_listener.stop()


if __name__ == "__main__":
    main()
