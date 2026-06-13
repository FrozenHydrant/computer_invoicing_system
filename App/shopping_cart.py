from typing import Tuple
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

from iteminfo_window_handle import IteminfoWindowHandle
from Datatypes.item import Item

# Handles the cart tab and actions there
class Cart:
    
    def __init__(self, root: Misc):
        # Pop-up window handler
        self.iteminfo_window_handle = IteminfoWindowHandle(root, self)

        # Initialize the main cart frame
        self.main_frame = Frame(root)
        self.main_frame.grid()

        self.cart_frame = Frame(self.main_frame)
        self.cart_frame.grid(row=0, column=0)

        self.button_frame = Frame(self.main_frame)
        self.button_frame.grid(row=0, column=1)

        # Custom fonts
        self.title_font = tkFont.Font(family="Arial", size=12)
        self.list_font = tkFont.Font(family="Arial", size=20)

        # Style
        self.style = Style()
        self.style.configure("TButton", padding=10, font=self.title_font)
        self.style.configure("TLabel", font=self.title_font)
        self.style.configure("TEntry", padding=5)

        # Variables
        self.items: list[Item] = []
        self.cart_items_display = Variable(value=[])
        self.selected_item = None
        self.selected_item_pos = -1

        # Labels
        items_label = Label(self.cart_frame, text="Items in Cart:")
        items_label.grid(row=0, column=0, padx=0, pady=10)

        self.selected_item_label = Label(self.main_frame, text="Selected Item: None")
        self.selected_item_label.grid(row=0, column=2, padx=200, pady=50)

        # Listbox with all cart items
        self.cart_listbox = Listbox(self.cart_frame, width=50, height=20, listvariable=self.cart_items_display, font=self.list_font)
        self.cart_listbox.grid(row=1, column=0, padx=10, pady=10)
        self.cart_listbox.bind("<<ListboxSelect>>", self._select_items)

        # Add item button
        self.add_item_button = Button(self.button_frame, text="Add Item", width=25, command=self._add_item, state=ACTIVE)
        self.add_item_button.grid(row=0, column=1, pady=10)

        # Delete selected button 
        self.delete_selected_button = Button(self.button_frame, text="Delete Selected Item", width=25, command=self._delete_item, state=ACTIVE)
        self.delete_selected_button.grid(row=1,column=1,pady=10)

        # Create Invoice button
        self.create_invoice_button = Button(self.button_frame, text="Create Invoice", width=25, state=ACTIVE)
        self.create_invoice_button.grid(row=2,column=1,pady=10)

    def _delete_item(self):
        if self.selected_item is not None:
            self.items.pop(self.selected_item_pos)

            # After an item is deleted, next item is selected, given it exists...
            if self.selected_item_pos < len(self.items):
                self.selected_item = self.items[self.selected_item_pos]
            else:
                self.selected_item_pos = -1
                self.selected_item = None

            # Then update the display
            self.update_display()


    def _add_item(self):
        self.iteminfo_window_handle.create()


    def update_display(self):
        display_items: list[str] = []
        for item in self.items:
            display_items.append(item.title)
        self.cart_items_display.set(display_items)

        selected_label_text = "Selected Item: None"
        if self.selected_item is not None:
            selected_label_text = "Selected Item: " + self.selected_item.title + "\n" + "Price: " + str(self.selected_item.price) + "\n" + "Cost: " + str(self.selected_item.cost)
        self.selected_item_label.config(text=selected_label_text)


    def locate_item(self, item_name: str) -> Tuple[int, Item] | None:
        for i, item in enumerate(self.items):
            if item.title == item_name:
                return (i, item)
        
        return None

    
    def _select_items(self, event):
        #print(self.cart_listbox.curselection())
        item_selection = self.cart_listbox.curselection()
        item_index: int = -1
        if len(item_selection) > 0:
            item_index = item_selection[0]
        else:
            return
        
        item_name = self.cart_items_display.get()[item_index]
        
        index, my_item = self.locate_item(item_name)
        if my_item is None:
            return
        
        # Update global state of selected item 
        self.selected_item = my_item
        self.selected_item_pos = index
        self.update_display()

