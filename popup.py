import tkinter as tk
from PIL import Image, ImageTk
import pygame


root = tk.Tk()
root.withdraw()

pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.mixer.init()

fluffy_cloud_image = Image.open("assets/fluffy_cloud.png").resize((640, 640), Image.LANCZOS)
christmas_tree_image = Image.open("assets/christmas_tree.png").resize((640, 640), Image.LANCZOS)
nonsense_image = Image.open("assets/spoodomotor.png").resize((640, 640), Image.LANCZOS)
boom = pygame.mixer.Sound("assets/vine_boom.wav")


def open_popup(type):
    """
    Opens a new popup
    
    :param type: "fluffy cloud" or "christmas tree"
    """
    if type == "fluffy cloud":
        _create_popup(fluffy_cloud_image.copy())
    elif type == "christmas tree":
        _create_popup(christmas_tree_image.copy())
    else:
        _create_popup(nonsense_image.copy())
    boom.play()


def _setup():
    # root.overrideredirect(True)
    # root.wm_attributes("-transparentcolor", '#000000')

    # 3. Set size and position
    width = 640
    height = 640
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)  # Center
    y = (screen_height // 2) - (height // 2)    # Center
    root.geometry(f'{width}x{height}+{x}+{y}')


def _create_popup(image):
    # 1. Create the main window
    popup = tk.Toplevel(root)

    # 2. Make the window borderless
    popup.overrideredirect(True)
    # popup.attributes('-alpha', 0.5)
    # Currently Only Supports Windows
    popup.wm_attributes("-transparentcolor", '#000000')

    # 3. Set size and position
    width = 640
    height = 640
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)  # Center
    y = (screen_height // 2) - (height // 2)    # Center
    popup.geometry(f'{width}x{height}+{x}+{y}')

    # 4. Add UI elements
    tk_image = ImageTk.PhotoImage(image)
    image_label = tk.Label(popup, image=tk_image, bg='#000000')
    image_label.image = tk_image  # Prevents garbage collection
    image_label.pack(expand=True, fill='both')

    # 5. Set up the 5-second timer (5000 milliseconds)
    popup.after(3000, _close_app, popup)


def _close_app(root):
    root.destroy()  # Closes the window completely


initialized = False
def init():
    global initialized
    if not initialized:
        initialized = True
        root.after(0, lambda: _setup)
        root.mainloop()