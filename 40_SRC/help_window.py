"""
Help Window Module

USE:
    This module provides a help window for the Guitar Tab Writer application.
"""

##################
# IMPORT SECTION
##################
# STANDARD libraries
from tkinter import Toplevel, Label, Button  # For GUI


###########
# CONSTANTS
###########
HLP_USE = "Permet d'écrire facilement et rapidement des tablatures."
HLP_CMD_1 = "Ctrl + DEL:\tSupprime la colonne courante."
HLP_CMD_2 = "Ctrl + H:\t\tAffiche cette fenêtre."
HELP_CONTENT = HLP_USE + "\n\n" + HLP_CMD_1 + '\n' + HLP_CMD_2



##################
# CLASS DEFINITION
##################
class HelpWindow:
    """
    Help Window class that handles the GUI and functionality.
    """
    def __init__(self, parent):
        """
        Initialize the Help Window.

        :param parent: The parent Tkinter window.
        """
        self.parent = parent

        # Create the help window
        self.window = Toplevel(parent)
        self.window.title("Guitar Tab Writer: Help")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.geometry("400x150")

        # Create a Label for the help content
        l_help_content = HELP_CONTENT
        l_help_label = Label(
            self.window,
            text=l_help_content, justify="left", wraplength=700, font=("Arial", 10))
        l_help_label.pack(padx=20, pady=20)

        # Create an OK Button
        l_ok_button = Button(self.window, text="OK", command=self.window.destroy, default="active")
        l_ok_button.pack(pady=(10, 0))

        # Set the focus to the OK Button
        l_ok_button.focus_set()

        # Bind the "Escape" key to close the HelpWindow
        self.window.bind("<Escape>", lambda event: self.window.destroy())

        return
    # end of function

# end of class

# End of file
