from tkinter import *
from tkinter.ttk import *
from enum import Enum

# Whether the entry field is Monetary or String or Numeric 
class InputType(Enum):
    STRING = 0
    MONETARY = 1
    NUMERIC = 2

# Creates the pop-up dialog when we try to add a new item
# 
class IteminfoWindowHandle:
    
    def __init__(self, root):
        self.entry_boxes = {}
        self.window = None
        self.window_is_open = False
        self.root = root


    def create(self):
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

        entry = Entry(self.main_frame)
        entry.grid(row=offset, column=1, pady=5)

        # TODO: make sure input fields are valid
        if type == InputType.MONETARY:
            pass
        elif type == InputType.STRING:
            pass
        elif type == InputType.NUMERIC:
            pass
        else:
            raise Exception("Invalid input type specified for entry field: " + name)

        self.entry_boxes[id] = entry
    

    def _confirm_create_item(self):
        # TODO: create item
        self._close()
        return None


    def _close(self):
        print("ItemInfo Window Destroyed.")
        self.window_is_open = False
        self.window.destroy()