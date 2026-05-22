from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkFont

from shopping_cart import Cart

# Main handler for our entire application
class App:
    root: Tk = None
    custom_font = None
    main_frame: Frame = None 
    tab_panel: Notebook = None
    cart: Cart = None
    instance = None


    def __init__(self):
        if App.instance is not None:
            raise Exception("Should not have more than one app at a time")

        # Initialize window
        App.root = Tk()
        App.root.geometry("1920x1080")

        # Special font
        App.custom_font = tkFont.Font(family='Arial', size=12)

        # The main frame which holds every other component
        App.main_frame = Frame(App.root)
        App.main_frame.grid()
        
        # Tab panel on the top "Cart, Quotation, Returns, Settings"
        App.tab_panel = Notebook(App.main_frame)

        # Sub-objects for each tab
        App.cart = Cart(App.tab_panel)

        z = Frame(App.tab_panel, padding=3)
        z.grid()
        zg = Label(z, text="Test 2", font=App.custom_font)
        zg.grid()

        # Add subobjects to tab panel
        App.tab_panel.add(App.cart.main_frame, text="Cart")
        App.tab_panel.add(z, text="Tab 2")
        App.tab_panel.grid(column=0, row=0, sticky="NW")

        App.instance = self


    def start(self):
        App.root.mainloop()

app: App = App()

if __name__ == "__main__":
    app.start()