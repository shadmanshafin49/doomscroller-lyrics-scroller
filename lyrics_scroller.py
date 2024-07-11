import tkinter as tk
from tkinter import ttk
import time
import threading

paused = False  # Global variable to track pause state
scroll_thread = None  # Global variable to store the scroll thread
y_position = None  # Global variable to track scroll position
font_size = 12  # Initial font size
line_spacing = 30  # Adjust line spacing as desired

# Color themes
light_theme = {
    "bg": "#f0f0f0",  # Light gray background
    "fg": "black",    # Black text color
    "canvas_bg": "white",  # White canvas background
    "button_bg": "#4285F4",  # Google blue
    "button_fg": "white"     # White text color for buttons
}

maroon_theme = {
    "bg": "#800000",   # Maroon background
    "fg": "white",     # White text color
    "canvas_bg": "#800000",  # Maroon canvas background
    "button_bg": "#400000",  # Google blue (dark)
    "button_fg": "white"     # White text color for buttons
}

dark_theme = {
    "bg": "#202124",   # Dark background
    "fg": "white",     # White text color
    "canvas_bg": "#121212",  # Dark canvas background
    "button_bg": "#1a73e8",  # Google blue (dark)
    "button_fg": "white"     # White text color for buttons
}



current_theme = light_theme  # Initial theme

def apply_theme(theme):
    root.configure(bg=theme["bg"])
    input_frame.configure(bg=theme["bg"])
    output_frame.configure(bg=theme["bg"])
    text_input.configure(bg=theme["bg"], fg=theme["fg"], font=("Segoe UI", 12))  # Modern font
    canvas.configure(bg=theme["canvas_bg"])
    increase_font_button.configure(bg=theme["button_bg"], fg=theme["button_fg"], font=("Segoe UI", 10, "bold"))  # Bold button font
    decrease_font_button.configure(bg=theme["button_bg"], fg=theme["button_fg"], font=("Segoe UI", 10, "bold"))  # Bold button font
    scroll_speed.configure(bg=theme["bg"], fg=theme["fg"], troughcolor=theme["bg"], activebackground=theme["button_bg"])
    scroll_button.configure(bg=theme["button_bg"], fg=theme["button_fg"], font=("Segoe UI", 10, "bold"))  # Bold button font
    pause_resume_button.configure(bg=theme["button_bg"], fg=theme["button_fg"], font=("Segoe UI", 10, "bold"))  # Bold button font

def toggle_theme():
    global current_theme
    if current_theme == light_theme:
        current_theme = maroon_theme
    elif current_theme==maroon_theme:
        current_theme = dark_theme
    elif current_theme==dark_theme:
        current_theme = light_theme
    apply_theme(current_theme)

def scroll_lyrics():
    global paused, y_position, font_size, line_spacing
    lyrics = text_input.get("1.0", tk.END)  # Get lyrics from text input
    lines = lyrics.splitlines()  # Split lyrics into lines

    y_position = canvas_height  # Start from the bottom of the canvas

    while y_position > -line_spacing * len(lines):
        if not paused:
            canvas.delete("all")  # Clear canvas
            for idx, line in enumerate(lines):
                canvas.create_text(canvas_width / 2, y_position + idx * line_spacing, text=line, anchor="center", font=("Segoe UI", font_size), fill=current_theme["fg"])
            y_position -= scroll_speed.get()  # Adjust speed dynamically
            root.update()  # Update the GUI
        time.sleep(0.05)  # Adjust scroll speed (smaller values for faster scroll)

def start_scroll():
    global scroll_thread, y_position
    if scroll_thread and scroll_thread.is_alive():
        return  # Don't start another thread if one is already running

    paused = False  # Ensure scrolling starts from the beginning
    y_position = None  # Reset y_position to start from the top
    scroll_thread = threading.Thread(target=scroll_lyrics)
    scroll_thread.start()

def toggle_pause_resume():
    global paused
    paused = not paused
    if paused:
        pause_resume_button.config(text="Resume")
    else:
        pause_resume_button.config(text="Pause")
        start_scroll()  # Resume scrolling when button is clicked

def increase_font_size():
    global font_size
    font_size += 2  # Increase font size by 2 points
    start_scroll()  # Restart scrolling to apply font size change

def decrease_font_size():
    global font_size
    if font_size > 2:
        font_size -= 2  # Decrease font size by 2 points
        start_scroll()  # Restart scrolling to apply font size change

def on_mouse_wheel(event):
    global y_position
    if event.delta > 0:  # Scroll up
        canvas.yview_scroll(-1, "units")
        y_position += 10  # Adjust scroll position
    elif event.delta < 0:  # Scroll down
        canvas.yview_scroll(1, "units")
        y_position -= 10  # Adjust scroll position

# Create the main application window
root = tk.Tk()
root.title("Lyrics Scroller")
root.configure(bg=light_theme["bg"])

# Constants
canvas_width = 600
canvas_height = 600

# Create a frame to hold input text area and buttons on the left
input_frame = tk.Frame(root, bg=light_theme["bg"])
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create a text input area for lyrics
text_input = tk.Text(input_frame, height=20, width=50, bg=light_theme["bg"], fg=light_theme["fg"], font=("Segoe UI", 12))
text_input.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create buttons for font size control
increase_font_button = tk.Button(input_frame, text="Increase Font Size", command=increase_font_size, bg=light_theme["button_bg"], fg=light_theme["button_fg"], font=("Segoe UI", 10, "bold"))
increase_font_button.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

decrease_font_button = tk.Button(input_frame, text="Decrease Font Size", command=decrease_font_size, bg=light_theme["button_bg"], fg=light_theme["button_fg"], font=("Segoe UI", 10, "bold"))
decrease_font_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

# Create a frame to hold the canvas and scrolling controls on the left
output_frame = tk.Frame(root, bg=light_theme["bg"])
output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Create a canvas widget to display scrolling text
canvas = tk.Canvas(output_frame, width=canvas_width, height=canvas_height, bg=light_theme["canvas_bg"])
canvas.pack()

# Create a scale for scroll speed control
scroll_speed = tk.Scale(output_frame, from_=1, to=20, orient=tk.HORIZONTAL, label="Scroll Speed", bg=light_theme["bg"], fg=light_theme["fg"], troughcolor=light_theme["bg"], activebackground=light_theme["button_bg"])
scroll_speed.pack()

# Create a scroll button
scroll_button = tk.Button(output_frame, text="Scroll", command=start_scroll, bg=light_theme["button_bg"], fg=light_theme["button_fg"], font=("Segoe UI", 10, "bold"))
scroll_button.pack()

# Create a pause/resume button
pause_resume_button = tk.Button(output_frame, text="Pause", command=toggle_pause_resume, bg=light_theme["button_bg"], fg=light_theme["button_fg"], font=("Segoe UI", 10, "bold"))
pause_resume_button.pack()

# Create a theme toggle button
theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme, bg=light_theme["button_bg"], fg=light_theme["button_fg"])
theme_button.grid(row=1, column=0, columnspan=2, pady=10)

# Bind mouse wheel events to canvas for scrolling
canvas.bind("<MouseWheel>", on_mouse_wheel)

# Apply initial theme
apply_theme(light_theme)

# Configure grid weights to make the frames expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Start the main event loop
root.mainloop()
