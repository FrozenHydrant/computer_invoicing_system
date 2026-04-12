from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

from iteminfo_window_handle import IteminfoWindowHandle

# Handles the cart tab and actions there
class Cart:
    
    def __init__(self, root):
        # Pop-up window handler
        self.iteminfo_window_handle = IteminfoWindowHandle(root)

        # Initialize the main cart frame
        self.main_frame = Frame(root)
        self.main_frame.grid()

        # Custom fonts
        self.title_font = tkFont.Font(family="Arial", size=12)
        self.list_font = tkFont.Font(family="Arial", size=20)

        # Style
        self.style = Style()
        self.style.configure("TButton", padding=10, font=self.title_font)
        self.style.configure("TLabel", font=self.title_font)
        self.style.configure("TEntry", padding=5)

        # Variables
        self.cart_items_display = Variable(value=[])

        items_label = Label(self.main_frame, text="Items in Cart:")
        items_label.grid(row=0, column=0, padx=0, pady=10)

        # Listbox with all cart items
        self.cart_listbox = Listbox(self.main_frame, width=50, height=20, listvariable=self.cart_items_display, font=self.list_font)
        self.cart_listbox.grid(row=1, column=0, padx=10, pady=10)

        # Add item button
        self.add_item_button = Button(self.main_frame, text="Add Item", width=25, command=self._add_item, state=ACTIVE)
        self.add_item_button.grid(row=1, column=1)

    def _add_item(self):
        self.iteminfo_window_handle.create()

