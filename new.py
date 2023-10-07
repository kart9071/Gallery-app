import tkinter as tk
from tkinter import Scrollbar, Canvas, Button, filedialog
from PIL import Image, ImageTk

# Create a function to scroll the canvas vertically
def scroll_canvas(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create a function to scroll the canvas horizontally
def scroll_canvas_horizontal(event):
    canvas.xview_scroll(-1 * (event.delta // 120), "units")

# Create a function to rotate the image
def rotate_image():
    global pil_image
    pil_image = pil_image.rotate(30)
    update_displayed_image()

# Create a function to save the rotated image to a file
def save_rotated_image():
    global pil_image
    if pil_image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            pil_image.save(save_path)

# Create a function to update the displayed image on the canvas
def update_displayed_image():
    global pil_image
    if pil_image:
        tk_image = ImageTk.PhotoImage(pil_image)
        canvas.itemconfig(image_on_canvas, image=tk_image)
        canvas.image = tk_image

# Create the main application window
root = tk.Tk()
root.title("Image Scrollbar Example")

# Create a Canvas widget to display the image
canvas = Canvas(root, width=400, height=300)
canvas.pack(fill="both", expand=True)

# Create a Scrollbar widget for vertical scrolling
scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to use the vertical scrollbar
canvas.config(yscrollcommand=scrollbar.set)

# Create a Scrollbar widget for horizontal scrolling
horizontal_scrollbar = Scrollbar(root, orient="horizontal", command=canvas.xview)
horizontal_scrollbar.pack(side="bottom", fill="x")

# Configure the canvas to use the horizontal scrollbar
canvas.config(xscrollcommand=horizontal_scrollbar.set)

# Load and display your image (replace 'image.gif' with your image file)
pil_image = Image.open('giphy.gif')
tk_image = ImageTk.PhotoImage(pil_image)
image_on_canvas = canvas.create_image(0, 0, anchor="nw", image=tk_image)
canvas.image = tk_image

# Bind the mouse wheel event to scroll the canvas vertically
canvas.bind("<MouseWheel>", scroll_canvas)

# Bind the mouse wheel event to scroll the canvas horizontally
canvas.bind("<Shift-MouseWheel>", scroll_canvas_horizontal)

# Create a "Rotate" button
rotate_button = Button(root, text="Rotate", command=rotate_image)
rotate_button.pack()

# Create a "Save" button
save_button = Button(root, text="Save", command=save_rotated_image)
save_button.pack()

root.mainloop()
