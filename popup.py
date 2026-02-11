import tkinter as tk
from PIL import Image, ImageTk
import threading


fluffy_cloud_image = Image.open("assets/fluffy_cloud.png").resize((640, 640), Image.LANCZOS)
christmas_tree_image = Image.open("assets/christmas_tree.png").resize((640, 640), Image.LANCZOS)
nonsense_image = Image.open("assets/spoodomotor.png").resize((640, 640), Image.LANCZOS)


def open_popup(type):
    """
    Opens a new popup
    
    :param type: "Fluffy Cloud" or "Christmas Tree"
    """
    if type == "Fluffy Cloud":
        _create_popup(fluffy_cloud_image)
    elif type == "Christmas Tree":
        _create_popup(christmas_tree_image)
    else:
        _create_popup(nonsense_image)


def _create_popup(image):
    # 1. Create the main window
    root = tk.Tk()

    # 2. Make the window borderless
    root.overrideredirect(True)
    # root.attributes('-alpha', 0.5)
    # Currently Only Supports Windows
    root.wm_attributes("-transparentcolor", '#000000')

    # 3. Set size and position
    width = 640
    height = 640
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)  # Center
    y = (screen_height // 2) - (height // 2)    # Center
    root.geometry(f'{width}x{height}+{x}+{y}')

    # 4. Add UI elements
    tk_image = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=tk_image, bg='#000000')
    image_label.image = tk_image  # Prevents garbage collection
    image_label.pack(expand=True, fill='both')

    # 5. Set up the 5-second timer (5000 milliseconds)
    root.after(3000, _close_app, root)

    # 6. Run the application
    root.mainloop()


def _close_app(root):
    root.destroy()  # Closes the window completely