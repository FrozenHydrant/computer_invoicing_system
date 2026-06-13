from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from Datatypes.gui import *
from Datatypes.item import *
from decimal import *


# Class for Subitems
class SubEntry:

    def __init__(self, root, offset: int, global_enabled: AwesomeCheckBox):
        # Make entry boxes
        self.name_entry = AwesomeEntryBox(root, InputType.STRING)
        self.price_entry = AwesomeEntryBox(root, InputType.MONETARY)
        self.cost_entry = AwesomeEntryBox(root, InputType.MONETARY)
        self.enabled_price_cost = AwesomeCheckBox(root, name="Price/Cost Enabled", callback=self.update_box_enables)
        self.name_entry.grid(row=offset, column=1)
        self.price_entry.grid(row=offset, column=3)
        self.cost_entry.grid(row=offset, column=5)
        self.enabled_price_cost.grid(row=offset, column=6)
        # Make labels
        price_label = Label(root, text="Price: ")
        cost_label = Label(root, text="Cost: ")
        #enabled_label = Label(root, text="Enabled: ")
        #price_enabled_label = Label(root, text="Price/Cost: ")
        self.global_enabled = global_enabled
        
        # Update once
        self.update_box_enables()

        price_label.grid(row=offset, column=2)
        cost_label.grid(row=offset, column=4)
    

    def update_box_enables(self) -> None:
        enable_price_cost = self.enabled_price_cost.get_value()
        if self.global_enabled.get_value():
            self.name_entry.config(state=ACTIVE)
            if enable_price_cost:
                self.price_entry.config(state=ACTIVE)
                self.cost_entry.config(state=ACTIVE)
            else:
                self.price_entry.config(state=DISABLED)
                self.cost_entry.config(state=DISABLED)
        else: 
            self.name_entry.config(state=DISABLED)
            self.price_entry.config(state=DISABLED)
            self.cost_entry.config(state=DISABLED)
    

    # Gets the value in a raw way, i.e all strings, no conversions
    def get_raw_value(self):
        info = {}
        info["name"] = self.name_entry.get_value()

        if self.global_enabled.get_value() and self.enabled_price_cost.get_value():
            info["price"] = self.price_entry.get_value()
            info["cost"] = self.cost_entry.get_value()

        return info


# Creates the pop-up dialog when we try to add a new item
# 
class IteminfoWindowHandle:
    
    def __init__(self, root: Misc, cart):
        self.entry_boxes: dict[str, AwesomeEntryBox] = {}
        self.subentries: dict[str, SubEntry] = {}
        self.enable_subitems = None
        self.window = None
        self.cart = cart
        self.window_is_open = False
        self.root = root


    def create(self) -> None:
        if not self.window_is_open:
            self.window = Toplevel(self.root)
            self.window.geometry("1280x720")
        
            # Setup frames to put our elements inside
            self.main_frame = Frame(self.window)
            self.main_frame.grid()
        
            self.top_frame = Frame(self.main_frame)
            self.top_frame.grid(row=0)

            self.bot_frame = Frame(self.main_frame)
            self.bot_frame.grid(row=1, pady=20, padx=20)

            # Create entry boxes and labels
            self._create_main_entry("Title", "title", 0, InputType.STRING)
            self._create_main_entry("Price", "price", 1, InputType.MONETARY)
            self._create_main_entry("Cost", "cost", 2, InputType.MONETARY)
            
            self.enable_subitems = AwesomeCheckBox(self.top_frame, name="Enable Subitems", callback=self._update_subentry_enables)
            self.enable_subitems.grid(row=2, column=2)

            self._create_sub_entry("CPU", "cpu", 0)
            self._create_sub_entry("GPU", "gpu", 1)
            self._create_sub_entry("RAM", "ram", 2)
            self._create_sub_entry("SSD", "ssd", 3)
            self._create_sub_entry("PSU", "psu", 4)
            self._create_sub_entry("Case", "case", 5)
            self._create_sub_entry("Cooler", "cooler", 6)
            self._create_sub_entry("Motherboard", "motherboard", 7)
            self._create_sub_entry("OS", "os", 8)

            self.confirmation_button = Button(self.main_frame, text="Create Item", command=self._confirm_create_item)
            self.confirmation_button.grid(row=3, column=3, pady=25)
            
            # Close the window properly, 
            self.window.protocol("WM_DELETE_WINDOW", self._close)
            self.window_is_open = True
    

    def _create_main_entry(self, name: str, id: str, offset: int, type: InputType):
        label = Label(self.top_frame, text=f"{name}: ")
        label.grid(row=offset, column=0, padx=20, pady=5)

        if type == InputType.MONETARY:
            pass
        elif type == InputType.STRING:
            pass
        elif type == InputType.NUMERIC:
            pass
        else:
            raise Exception("Invalid input type specified for entry field: " + name)
        
        entry = AwesomeEntryBox(self.top_frame, type)
        entry.grid(row=offset, column=1, pady=5)
        self.entry_boxes[id] = entry


    def _create_sub_entry(self, name: str, id: str, offset: int):
        # Subentries must be: Name, Cost, Price
        label = Label(self.bot_frame, text=f"{name}: ")
        label.grid(row=offset, column=0, padx=32)

        entry = SubEntry(self.bot_frame, offset, self.enable_subitems)
        self.subentries[id] = entry

    
    def _update_subentry_enables(self):
        for subentry in self.subentries.values():
            subentry.update_box_enables()

    
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
        # Create Subitems
        # TODO: allow $ sign when parsing price/cost
        if self.enable_subitems.get_value():
            for key, entry in self.subentries.items():
                # Hint https://stackoverflow.com/questions/41641449/how-do-i-annotate-types-in-a-for-loop
                entry: SubEntry
                sub_info = entry.get_raw_value()
                sub_name = sub_info["name"]
                sub_item = Item.SubItem(sub_name)

                # Extract price and cost
                if "price" in sub_info:
                    try:
                        price = Decimal(sub_info["price"])
                        sub_item.set_price(price)
                    except Exception as e:
                        print("Cannot create item due to bad subitem price", sub_info["price"], sub_name)
                        return None
                    
                if "cost" in sub_info:
                    try:
                        cost = Decimal(sub_info["cost"])
                        sub_item.set_cost(cost)
                    except Exception as e:
                        print("Cannot create item due to bad subitem cost", sub_info["cost"], sub_name)
                        return None

                my_item.add_subitem(key, sub_item)

        # Suspicious... TODO: fix?
        # Add the item to the cart and update display
        # Make sure item wasn't inside beforehand
        if self.cart.locate_item(title) is not None:
            # TODO: change to a message in the window
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