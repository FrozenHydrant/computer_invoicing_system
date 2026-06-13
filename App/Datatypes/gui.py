from tkinter import *
from tkinter.ttk import *
from enum import Enum
import re

# Whether the entry field is Monetary or String or Numeric 
class InputType(Enum):
    STRING = 0
    MONETARY = 1
    NUMERIC = 2


# Check Box Class with more info
class AwesomeCheckBox(Checkbutton):

    def __init__(self, root, name="", callback=None):
        self.status = BooleanVar()
        self.status.set(False)
        super().__init__(root, variable=self.status, command=callback, text=name)


    def get_value(self):
        return self.status.get()
    

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