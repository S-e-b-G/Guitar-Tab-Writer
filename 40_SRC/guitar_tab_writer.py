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
from tkinter import Tk, Text, font, Button  # For GUI
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
INITIAL_TAB = '\n'.join([f'{string}|' for string in STRINGS])  # Constant => pylint: disable=C0103

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
        self.text_zone = Text(self.root, font=self.font, width=100, height=6)
        self.text_zone.pack()

        # Insert the initial tab
        self.text_zone.insert('1.0', INITIAL_TAB)

        # Set the cursor to the end of the first line
        self.text_zone.mark_set("insert", "1.end")
        self.text_zone.see("insert")

        # Bind the insert event
        self.text_zone.bind('<KeyRelease>', self.on_key_release)

        # Create a Clear button
        self.clear_button = Button(self.root, 
                                   text="Clear", 
                                   command=self.clear_tab)
        self.clear_button.pack(side="left", padx=(0, 10), pady=(10, 0))

        # Create a Copy button
        self.copy_button = Button(  self.root, 
                                    text="Copy",
                                    command=self.copy_tab)
        self.copy_button.pack(side="left", padx=(0, 10), pady=(10, 0))

        # Create a Process button
        self.process_button = Button(self.root, 
                                     text="Process", 
                                     command=self.process_tab)
        self.process_button.pack(side="left", padx=(0, 10), pady=(10, 0))

        # Create a "-1 oct." button
        self.decrement_octave_button = Button(self.root, 
                                              text="-1 oct.", 
                                              command=self.decrement_octave)
        self.decrement_octave_button.pack(side="left", padx=(0, 10), pady=(10, 0))

        # Create a "+1 oct." button
        self.increment_octave_button = Button(self.root, 
                                              text="+1 oct.", 
                                              command=self.increment_octave)
        self.increment_octave_button.pack(side="left", padx=(0, 10), pady=(10, 0))

        # Create a Help button
        self.help_button = Button(self.root, text="Help", command=self.open_help_window)
        self.help_button.pack(side="left", pady=(10, 0))

        # Create a selectable text zone with the link
        self.link_text = Text(self.root,
                              font=self.font,
                              height=1, width=20,
                              wrap="none",
                              state="normal")
        self.link_text.pack(side="bottom", fill="x", pady=(10, 0))
        self.link_text.insert("1.0", "https://tabnabber.com/convert_guitar_sheet_music.asp")
        # Disable the possibility to modify the text
        self.link_text.config(state="disabled")

        # Set the focus to the text zone
        self.text_zone.focus_set()

        # Bind the TAB key to move focus to the Process button
        self.root.bind("<Tab>", lambda event: self.process_button.focus_set())

        # Bind the "Ctrl" + "H" key combination to open the help window
        self.root.bind("<Control-h>", self.open_help_window)
        self.root.bind("<Control-Shift-Delete>", self.clear_tab)

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
        # Get the text zone content
        text = self.text_zone.get('1.0', 'end-1c')

        # Get the cursor position and lines content
        cursor_position = self.text_zone.index("insert")
        cursor_row = int(cursor_position.split('.', maxsplit=1)[0]) - 1
        lines = text.split('\n')
        current_line = lines[cursor_row]
        line_length = len(current_line)
        cursor_col = int(cursor_position.split('.', maxsplit=1)[1])

        # Get the inserted information
        inserted_character = event.char
        inserted_keycode   = event.keycode
        if(inserted_keycode == 54 and event.state & 131116):
            # Corresponds to the "|" character
            inserted_character = '|'
        elif (inserted_character == '.'):
            # Make the '.' char behave as '|'
            inserted_character = '|'
            current_line = current_line[:cursor_col-1] + '|' + current_line[cursor_col:]
            lines[cursor_row] = current_line
        # else: no need to do anything

        # Display the current keycode, current char, current state
        # print(f"Keycode: {event.keycode}, Char: {event.char}, State: {event.state}")

        if (event.state & 0x0001) and (event.keycode == 46):
            # 0x0001 represents the SHIFT key, 46 represents the DEL key
            # Shift + Del => delete the characters for the current column
            self.handle_shift_del(cursor_position, text)

        elif inserted_character.isdigit():
            # Check if there is a "-" character to the right of the cursor

            # Check if it's the end of line
            if(cursor_col < line_length):
                # Not the end of the line: proceed
                next_char_position = self.text_zone.index('insert')
                    # Note: Not 'insert + 1c' as the character has already been inserted
                    # Then: self.text_zone.index('insert') is the character after the one inserted
                next_char = self.text_zone.get(next_char_position)
            else:
                #end of line: make as if next char is 0
                next_char = '0'
            #end if

            if next_char != '-':
                # Not a '-': insert it and add '-' on other lines
                self.handle_number_input(cursor_position, lines, inserted_character)
            else:
                # Next char is '-': Delete it
                lines[cursor_row] = \
                    current_line[:cursor_col] + current_line[cursor_col+1:]
                self.text_zone.delete('1.0', 'end')
                self.text_zone.insert('1.0', '\n'.join(lines))

                # Restore the cursor position
                new_cursor_position = \
                    f"{cursor_row + 1}.{int(cursor_position.split('.', maxsplit=1)[1])}"
                self.text_zone.mark_set("insert", new_cursor_position)
                self.text_zone.see("insert")
            # endif

        elif inserted_character == '-' or inserted_character == '|':
            self.handle_number_input(cursor_position, lines, inserted_character)

        # else not a character to handle

        return
    # end of function


    def clear_tab(self, event=None): # pylint: disable=unused-argument
        """
        Clear the tab by restoring its content to the initial state.
        """
        self.text_zone.delete('1.0', 'end')
        self.text_zone.insert('1.0', INITIAL_TAB)

        # Set the cursor to the end of the first line
        self.text_zone.mark_set("insert", "1.end")
        self.text_zone.see("insert")

        return
    # end of function


    def handle_shift_del(self, cursor_position, text):
        """
        Handle the Shift + Del key combination.

        :param cursor_position: The current cursor position.
        :param text: The current text in the text zone.
        """
        # Save the current cursor position
        cursor_position = self.text_zone.index("insert")

        lines = text.split('\n')
        # Get position
        # cursor_row = int(cursor_position.split('.', maxsplit=1)[0]) - 1
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

        return
    # end of function


    def handle_number_input(self, cursor_position, lines, inserted_character):
        """
        Handle the insertion of numbers, "-", or "|" characters.

        :param cursor_position: The current cursor position.
        :param lines: The lines of the current text in the text zone.
        :param inserted_character: The character to be inserted.
        """
        # Get position
        cursor_row = int(cursor_position.split('.', maxsplit=1)[0]) - 1
        cursor_col = int(cursor_position.split('.', maxsplit=1)[1])

        # Update the other lines
        line_len = len(lines[cursor_row])
        for i, _ in enumerate(lines):
            if i != cursor_row:
                if inserted_character == '|':
                    lines[i] = lines[i][:cursor_col-1] + '|' + lines[i][cursor_col-1:]
                    #lines[i] = lines[i] + '|'rh
                else:
                    for _ in range(len(lines[i]), line_len):
                        lines[i] = ( lines[i][:cursor_col-1] +
                                    '-' +
                                    lines[i][cursor_col-1:] )
                        #lines[i] = lines[i] + ('-' * (line_length - len(lines[i])))
                    # end for
                # endif
            #else: Current row, nothing to change
        #end for

        self.text_zone.delete('1.0', 'end')
        self.text_zone.insert('1.0', '\n'.join(lines))

        # Restore the cursor position
        new_cursor_position = \
            f"{cursor_row + 1}.{cursor_col}"
        self.text_zone.mark_set("insert", new_cursor_position)
        self.text_zone.see("insert")

        return
    # end of function


    def decrement_octave(self):
        """
        Decrement all numbers in the tab by 12.
        """
        l_DECR_VAL = 12 # pylint: disable=invalid-name
        # Get the text from the text zone
        l_text = self.text_zone.get('1.0', 'end-1c')
        # Split the text into lines
        l_lines = l_text.split('\n')

        for l_i, l_line in enumerate(l_lines):
            # Initialize an empty string to store the new line
            l_new_line = ''
            # Initialize a variable to store the previous character
            l_prev_char = 0

            l_dig_pos = 1   # Digit position in the number
            for l_char in l_line:
                # Iterate through each character in the line
                
                if l_char.isdigit():
                    # If the previous character is also a digit,
                    # it means the current digit is part of a multi-digit number
                    if( (int(l_char)<=2)    and
                        (l_dig_pos <= 1)    ):
                        # First of a 2-digit number
                        l_dig_pos+=1
                    else:
                        # End of the number
                        l_dig_pos = 1   # Reset for next char
                        # Decrement the current digit by 12 if it's greater than or equal to 12,
                        # otherwise replace it with '0'
                        l_num = int(str(l_prev_char)+l_char)
                        if l_num <= (9+l_DECR_VAL):
                            l_new_line += '-'
                        # else: still a 2-digit number: notheing to do
                        l_new_line += str(l_num - l_DECR_VAL if l_num >= l_DECR_VAL else '0')
                        # If new number is a 1-digit number, 
                        # add a '-' to the new line to preserve the column alignment
                    #endif
                else:
                    # Not a digit, add it to the new line as is
                    if l_dig_pos > 1:
                        # Insert the previous digit too (although this should not happen)
                        l_new_line += '0' # Previous digit -12 is < 0, so insert '0'
                        l_dig_pos = 1
                    # else: no previous char to take into account
                    if l_char == ' ':
                        l_new_line += '-'
                    else:
                        l_new_line += l_char
                    # endif
                #endif

                # Update the previous character
                if l_char.isdigit():
                    l_prev_char = int(l_char)
                else:
                    #Not a digit: change it to 0
                    l_prev_char = 0
                    l_dig_pos = 1   # Reset for next char
                # endif
            #endfor (characters in the line)

            if l_dig_pos > 1:
                # In case there would be a last char to process (although this should not happen)
                l_new_line += '0' # Previous digit -12 is < 0, so insert '0'
                l_dig_pos = 1
            # else: no last char to process

            # Replace the original line with the new line
            l_lines[l_i] = l_new_line
        #endfor (lines)

        # Clear the text zone and insert the updated text
        self.text_zone.delete('1.0', 'end')
        self.text_zone.insert('1.0', '\n'.join(l_lines))

        return
    # end of function


    def increment_octave(self):
        """
        Increment all numbers in the tab by 12.
        """
        # Constant
        l_INCR_VAL = 12  # pylint: disable=invalid-name

        # Get the text from the text zone
        l_text = self.text_zone.get('1.0', 'end-1c')
        # Split the text into lines
        l_lines = l_text.split('\n')

        for l_i, l_line in enumerate(l_lines):
            # Initialize an empty string to store the new line
            l_new_line = ''
            # Initialize a variable to store the previous character
            l_prev_char = 0

            # Initialize digit position in the number
            l_dig_pos = 1
            for l_col_nb, l_char in enumerate(l_line):
                # Iterate through each character in the line
                l_dash_on_lines = False

                if l_char.isdigit():
                    # Current char is digit (of a single or multi-digt number)
                    if ((int(l_char) <= 2) and (l_dig_pos <= 1)):
                        # First of a 2-digit number
                        l_dig_pos += 1
                    else:
                        # End of the number
                        if l_dig_pos <= 1:
                            # A 1-digit number will become a 2-digit number
                            l_dash_on_lines = True
                        #else: Was already a 2-digit number: nothing to do
                        l_dig_pos = 1  # Reset for next char
                        # Increment the current digit by 12
                        l_num = int(str(l_prev_char) + l_char)
                        l_new_line += str(l_num + l_INCR_VAL)
                    # end if
                else:
                    # If the character is not a digit, add it to the new line as is
                    if l_dig_pos > 1:
                        # Insert the previous digit too
                        l_new_line += str(l_prev_char + l_INCR_VAL)
                        l_dig_pos = 1
                        l_dash_on_lines = True
                    # else: no previous char to take into account

                    if l_char == ' ':
                        l_new_line += '-'
                    else:
                        l_new_line += l_char
                    # end if
                # end if

                # Update the previous character
                if l_char.isdigit():
                    l_prev_char = int(l_char)
                else:
                    # Not a digit: change it to 0
                    l_prev_char = 0
                    l_dig_pos = 1  # Reset for next char
                # end if
                
                # Add '-' on other lines if needed
                if l_dash_on_lines:
                    l_dash_on_lines = False
                    for l_line_nb, l_line_content in enumerate(l_lines):
                        # On all lines...
                        if l_line_nb != l_i:
                            # ... except the current one, add a '-' on current column position
                            l_lines[l_line_nb] = (
                                l_line_content[0:l_col_nb] + '-' + 
                                l_line_content[l_col_nb:])
                        # else: current line: nothing to do
                    #end for
                #else: no need to add '-'
            # end for (characters in the line)

            if l_dig_pos > 1:
                # In case there would be a char to process
                l_new_line += str(l_prev_char + l_INCR_VAL)
                l_dig_pos = 1
            #else: no other char to process

            # Replace the original line with the new line
            l_lines[l_i] = l_new_line
        # end for (lines)

        # Clear the text zone and insert the updated text
        self.text_zone.delete('1.0', 'end')
        self.text_zone.insert('1.0', '\n'.join(l_lines))

        return
    # end of function



    ##############################
    # PUBLIC FUNCTIONS
    ##############################
    def copy_tab(self):
        """
        Copy its content to the clipboard.
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

        return


    def process_tab(self):
        """
        Process the tab by copying its content to the clipboard and 
        opening a link in the default web browser.
        """
        # Copy the content to the clipboard
        self.copy_tab()

        # Open the link in the default web browser
        webbrowser.open("https://tabnabber.com/convert_guitar_sheet_music.asp")

        # Display a success message
        # messagebox.showinfo("Success", "Tab content has been saved and the link has been opened.")

        return


    def open_help_window(self, event=None): # pylint: disable=unused-argument
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
