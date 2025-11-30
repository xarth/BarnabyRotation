import tkinter as tk
from PIL import ImageTk, Image
import pyautogui

class RegionSelector:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None

        # Take a screenshot of the whole screen
        self.screenshot = pyautogui.screenshot()
        self.screenshot.save("screenshot.png")  # optional: save for debugging

        self.root = tk.Tk()
        self.root.title("Drag to select region")
        
        # Fullscreen window
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        
        # Convert screenshot for Tkinter
        self.img = ImageTk.PhotoImage(self.screenshot)
        self.canvas = tk.Canvas(self.root, width=self.screenshot.width, height=self.screenshot.height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.root.mainloop()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        # Draw a temporary rectangle
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)

        print("Region selected:")
        print(f"top = {top}, left = {left}, width = {width}, height = {height}")

        # Close the window after selection
        self.root.destroy()


if __name__ == "__main__":
    RegionSelector()