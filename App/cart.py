from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

class Cart:
    
    def __init__(self, root):
        # Initialize the main cart frame
        self.main_frame = Frame(root)
        self.main_frame.grid()

        # Custom fonts
        self.title_font = tkFont.Font(family="Arial", size=12)
        self.list_font = tkFont.Font(family="Arial", size=20)

        # Variables
        self.cart_items_display = Variable(value=[])

        items_label = Label(self.main_frame, text="Items in Cart:", font=self.title_font)
        items_label.grid(row=0, column=0, padx=0, pady=10)

        # Listbox with all cart items
        self.cart_listbox = Listbox(self.main_frame, width=50, height=20, listvariable=self.cart_items_display, font=self.list_font)
        self.cart_listbox.grid(row=1, column=0, padx=10, pady=10)

        # Add item button
        self.add_item_button = Button(self.main_frame, text="Add Item")
        self.add_item_button.grid()