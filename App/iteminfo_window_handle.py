from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import re
from enum import Enum
from decimal import *
from Datatypes.item import *

# Whether the entry field is Monetary or String or Numeric 
class InputType(Enum):
    STRING = 0
    MONETARY = 1
    NUMERIC = 2


# Entry Box Class with more info
class AwesomeEntryBox(Entry):

    def __init__(self, root, ft: InputType):
        self.filter_type = ft
        self.string_variable = StringVar()
        self.string_variable.trace_add("write", self._ensure_valid_entry)
        super().__init__(root, textvariable=self.string_variable)

    # Make sure the text inputted in the box is valid for its type
    # Monetary/numeric = only numbers
    def _ensure_valid_entry(self, var, index, mode):
        if self.filter_type == InputType.MONETARY:
            # TODO: better filtering
            my_string = self.string_variable.get()
            my_string = re.sub(r"[^0-9$.]", "", my_string)
            self.string_variable.set(my_string)

    
    def get_value(self) -> str:
        return self.string_variable.get()
    

# Creates the pop-up dialog when we try to add a new item
# 
class IteminfoWindowHandle:
    
    def __init__(self, root: Misc, cart):
        self.entry_boxes: dict[str, AwesomeEntryBox] = {}
        self.window = None
        self.cart = cart
        self.window_is_open = False
        self.root = root


    def create(self) -> None:
        if not self.window_is_open:
            self.window = Toplevel(self.root)
            self.window.geometry("640x480")
        
            self.main_frame = Frame(self.window)
            self.main_frame.grid()
        
            # Create entry boxes and labels
            self._create_main_entry("Title", "title", 0, InputType.STRING)
            self._create_main_entry("Price", "price", 1, InputType.MONETARY)
            self._create_main_entry("Cost", "cost", 2, InputType.MONETARY)

            self.confirmation_button = Button(self.main_frame, text="Create Item", command=self._confirm_create_item)
            self.confirmation_button.grid(row=3, column=3, pady=25)
            
            # Close the window properly, 
            self.window.protocol("WM_DELETE_WINDOW", self._close)
            self.window_is_open = True
    

    def _create_main_entry(self, name: str, id: str, offset: int, type: InputType):
        label = Label(self.main_frame, text=f"{name}: ")
        label.grid(row=offset, column=0, padx=20, pady=5)


        if type == InputType.MONETARY:
            pass
        elif type == InputType.STRING:
            pass
        elif type == InputType.NUMERIC:
            pass
        else:
            raise Exception("Invalid input type specified for entry field: " + name)
        
        entry = AwesomeEntryBox(self.main_frame, type)
        entry.grid(row=offset, column=1, pady=5)
        self.entry_boxes[id] = entry
    

    def _confirm_create_item(self) -> None:
        # TODO: create item
        title = self.entry_boxes["title"].get_value()
        price = self.entry_boxes["price"].get_value()
        cost = self.entry_boxes["cost"].get_value()

        try:
            price = Decimal(price)
            cost = Decimal(cost)
        except Exception as e:
            print("Cannot create item, ", e)
            return None

        my_item = Item(title, price, cost)
        # Suspicious... TODO: fix?
        # Add the item to the cart and update display
        # Make sure item wasn't inside beforehand
        if self.cart.locate_item(title) is not None:
            messagebox.showerror("Item Creation Problem", "Cannot make an item with the same name as an existing one.")
        else:
            self.cart.items.append(my_item) 
            self.cart.update_display()
            self._close()
        return None


    def _close(self):
        #print("ItemInfo Window Destroyed.")
        self.window_is_open = False
        self.window.destroy()