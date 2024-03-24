"""
Guitar Tab Writer Application

USE:
    This application provides a simple text zone for writing guitar tabs. It automatically
    aligns the text and inserts hyphens or bars as necessary.
"""

##################
# IMPORT SECTION
##################
# STANDARD libraries
import webbrowser           # For opening the link in the default web browser
from tkinter import Tk, Text, font, Button, messagebox  # For GUI
from pyperclip import copy  # For clipboard copy
from help_window import HelpWindow  # For the help window

##################
# GLOBAL CONSTANTS
##################
# GUI
APP_TITLE = 'Guitar Tab Writer'  # Constant => pylint: disable=C0103
FONT_FAMILY = 'Courier'  # Constant => pylint: disable=C0103
FONT_SIZE = 12  # Constant => pylint: disable=C0103

# Guitar Tab
STRINGS = ['e', 'b', 'g', 'd', 'a', 'e']  # Constant => pylint: disable=C0103
INITIAL_TAB = '\n'.join([f'{string}|-' for string in STRINGS])  # Constant => pylint: disable=C0103

##################
# CLASS DEFINITION
##################
class GuitarTabWriter:
    """
    Guitar Tab Writer class that handles the GUI and functionality.
    """
    def __init__(self, root):
        """
        Initialize the Guitar Tab Writer Application.

        :param root: The root Tkinter window.
        """
        self.root = root
        self.root.title(APP_TITLE)

        # Create a monospaced font
        self.font = font.Font(family=FONT_FAMILY, size=FONT_SIZE)

        # Create a text zone
        self.text_zone = Text(self.root, font=self.font, height=6)
        self.text_zone.pack()

        # Insert the initial tab
        self.text_zone.insert('1.0', INITIAL_TAB)

        # Set the cursor to the end of the first line
        self.text_zone.mark_set("insert", "1.end")
        self.text_zone.see("insert")

        # Bind the insert event
        self.text_zone.bind('<KeyRelease>', self.on_key_release)

        # Create a Process button
        self.process_button = Button(self.root, text="Process", command=self.process_tab)
        self.process_button.pack(side="left", padx=(0, 10), pady=(10, 0))

        # Create a Help button
        self.help_button = Button(self.root, text="Help", command=self.open_help_window)
        self.help_button.pack(side="left", pady=(10, 0))

        # Set the focus to the text zone
        self.text_zone.focus_set()

        # Bind the TAB key to move focus to the Process button
        self.root.bind("<Tab>", lambda event: self.process_button.focus_set())

        # Bind the "Ctrl" + "H" key combination to open the help window
        self.root.bind("<Control-h>", self.open_help_window)

        return
    # end of function


    ##############################
    # PRIVATE FUNCTIONS
    ##############################
    def on_key_release(self, event):
        """
        Handle key release events.

        :param event: The key release event.
        """
        text = self.text_zone.get('1.0', 'end-1c')
        cursor_position = self.text_zone.index('insert')

        inserted_character = event.char
        inserted_keycode   = event.keycode
        if(inserted_keycode == 54 and event.state & 131116):
            # Corresponds to the "|" character
            inserted_character = '|'
        # else: no need to do anything

        # Display the current keycode, current char, current state
        # print(f"Keycode: {event.keycode}, Char: {event.char}, State: {event.state}")

        if (event.state & 0x0001) and (event.keycode == 46):
            # 0x0001 represents the SHIFT key, 46 represents the DEL key

            # Save the current cursor position
            cursor_position = self.text_zone.index("insert")

            # Shift + Del => delete the characters for the current column
            lines = text.split('\n')
            # Get position
            cursor_row = int(cursor_position.split('.', maxsplit=1)[0]) - 1
            cursor_col = int(cursor_position.split('.', maxsplit=1)[1])

            # Delete characters
            for i, line in enumerate(lines):
                if len(line) > cursor_col:
                    lines[i] = lines[i][:cursor_col] + lines[i][cursor_col + 1:]
                # else: end of line
            # end for

            # Rebuild text zone
            self.text_zone.delete('1.0', 'end')
            self.text_zone.insert('1.0', '\n'.join(lines))

            # Restore the cursor position
            self.text_zone.mark_set("insert", cursor_position)
            self.text_zone.see("insert")


        elif inserted_character.isdigit() or inserted_character == '-' or inserted_character == '|':
            # Save the current cursor position
            cursor_position = self.text_zone.index("insert")

            lines = text.split('\n')
            cursor_row = (int(cursor_position.split('.', maxsplit=1)[0]))-1

            # Check if the cursor is at the end of the text
            if cursor_row >= len(lines):
                cursor_row -= 1

            current_line = lines[cursor_row]
            line_length = len(current_line)

            for i, _ in enumerate(lines):
                if i != cursor_row:
                    if inserted_character == '|':
                        lines[i] = lines[i] + '|'
                    else:
                        lines[i] = lines[i] + ('-' * (line_length-len(lines[i])))

            self.text_zone.delete('1.0', 'end')
            self.text_zone.insert('1.0', '\n'.join(lines))

            # Restore the cursor position
            self.text_zone.mark_set("insert", cursor_position)
            self.text_zone.see("insert")

        return
    # end of function

#end class



    ##############################
    # PUBLIC FUNCTIONS
    ##############################
    def process_tab(self):
        """
        Process the tab by saving its content to a file, opening a link in the default web browser,
        and displaying a success message.
        """
        # Get the content of the text zone
        tab_content = self.text_zone.get("1.0", "end-1c")

        # # Save the content to a file
        # file_path = asksaveasfilename(
            # defaultextension=".txt",
            # filetypes=[("Text Files", "*.txt")])
        # if file_path:
        #     with open(file_path, "w", encoding="utf-8") as file:
        #         file.write(tab_content)

        # Save the content to the clipboard
        # Copy the tab content to the clipboard
        copy(tab_content)

        # Open the link in the default web browser
        webbrowser.open("https://tabnabber.com/convert_guitar_sheet_music.asp")

        # Display a success message
        messagebox.showinfo("Success", "Tab content has been saved and the link has been opened.")

        return


    def open_help_window(self, event=None):
        """
        Open the help window.
        """
        HelpWindow(self.root)
        return
    # end of function

#end class



##################
# MAIN FUNCTION
##################
def main():
    """
    Main function to start the application.
    """
    root = Tk()
    GuitarTabWriter(root)
    root.mainloop()

    return
# end function

if __name__ == '__main__':
    main()

# End of file
