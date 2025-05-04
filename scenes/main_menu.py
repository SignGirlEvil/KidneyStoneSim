import tkinter as tk


class MainMenuFrame(tk.Frame):
    def __init__(self, master: tk.Tk, graphic_config: dict, **kwargs):
        super().__init__(master, **kwargs)

        # Make it so the items in the main menu move appropriately if the window is resized
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Create a label and add it to the main menu's grid
        tk.Label(
            self,
            text='Main Menu! :D',
            fg='black',  # 'fg' = 'foreground' (text color)
            bg=self['bg']
        ).grid(row=0, column=0, padx=10, pady=10)

        # Create a button and add it to the main menu's grid
        tk.Button(
            self,
            text='Press if you have kidneys'
        ).grid(row=1, column=0, stick='ew', padx=10, pady=10)  # Sticking is gross, which is why I say 'ew'
