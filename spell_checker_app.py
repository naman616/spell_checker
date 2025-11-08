import tkinter as tk
from tkinter import ttk, Menu, Text, messagebox
import re
from spellchecker import SpellChecker



class SpellCheckerApp:
    def __init__(self, root):
        """
        Initialize the Spell Checker Application.
        """
        self.root = root
        self.root.title("AI-Powered Real-Time Spell Checker")
        self.root.geometry("800x600")

        # Initialize the SpellChecker object.
        # This object contains the dictionary (like a Hash Map)
        # and methods for correction (Levenshtein distance).
        self.spell = SpellChecker()

        # --- Main Text Widget ---
        self.text_widget = Text(self.root, 
                                font=("Inter", 12), 
                                wrap="word", 
                                undo=True,  # Enable undo/redo
                                selectbackground="#add8e6", # Light blue selection
                                borderwidth=2, 
                                relief="groove")
        self.text_widget.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        # --- Status Bar (Optional, but good) ---
        self.status_bar = ttk.Label(self.root, text="Ready", anchor="w")
        self.status_bar.pack(fill="x", padx=10, pady=(5, 10))

        # --- Configure Tags for Highlighting ---
        # This is the core of the "red underline" feature.
        self.text_widget.tag_configure("misspelled", 
                                       foreground="red", 
                                       underline=True)

        # --- Right-Click Context Menu for Suggestions ---
        self.suggestion_menu = Menu(self.root, tearoff=0)
        
        # --- Bind Events ---
        # 1. <KeyRelease>: Fired every time the user lifts a key.
        #    This triggers the real-time spell check.
        self.text_widget.bind("<KeyRelease>", self.check_spelling)
        
        # 2. <Button-3>: Fired on right-click.
        #    This will show the suggestion menu.
        self.text_widget.bind("<Button-3>", self.show_suggestions)
        
        # 3. <Control-z> and <Control-y> for undo/redo
        self.root.bind_all("<Control-z>", self.text_widget.edit_undo)
        self.root.bind_all("<Control-y>", self.text_widget.edit_redo)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.update_status("App loaded. Type to begin spell checking.")

    def update_status(self, message):
        """Updates the text in the status bar."""
        self.status_bar.config(text=message)

    def check_spelling(self, event=None):
        """
        Event handler for <KeyRelease>.
        Scans the entire text widget for spelling errors and applies tags.
        """
        
        # 1. Remove all existing "misspelled" tags.
        # This is simpler than tracking individual word changes.
        self.text_widget.tag_remove("misspelled", "1.0", "end")

        # 2. Get all content from the text widget.
        content = self.text_widget.get("1.0", "end-1c")

        # 3. Use regex to find all words.
        # \b matches a word boundary. \w+ matches one or more word characters.
        # This is more efficient than splitting by space, as it handles punctuation.
        words_found = 0
        errors_found = 0
        for match in re.finditer(r'\b\w+\b', content):
            words_found += 1
            word = match.group(0)
            
            # 4. Check if the word is unknown.
            # self.spell.unknown() takes a list and returns a set of unknown words.
            # We check if our word (in lowercase) is in the unknown set.
            if word.lower() in self.spell.unknown([word.lower()]):
                errors_found += 1
                
                # 5. If unknown, get the start and end index from the match object.
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                
                # 6. Apply the "misspelled" tag to this range.
                self.text_widget.tag_add("misspelled", start, end)
        
        self.update_status(f"Words: {words_found} | Errors Found: {errors_found}")

    def show_suggestions(self, event):
        """
        Event handler for <Button-3> (Right-Click).
        Displays a context menu with spelling suggestions if a misspelled
        word is clicked.
        """
        
        # 1. Clear any old items from the suggestion menu.
        self.suggestion_menu.delete(0, "end")

        # 2. Get the index of the text widget at the click position.
        click_index = self.text_widget.index(f"@{event.x},{event.y}")

        # 3. Get the list of tags at that specific index.
        tags_at_click = self.text_widget.tag_names(click_index)

        # 4. Check if "misspelled" is one of the tags.
        if "misspelled" in tags_at_click:
            # 5. Get the start and end of the word at the click index.
            word_start = self.text_widget.index(f"{click_index} wordstart")
            word_end = self.text_widget.index(f"{click_index} wordend")
            
            # Get the actual misspelled word.
            word = self.text_widget.get(word_start, word_end)

            # 6. Get correction candidates from the pyspellchecker library.
            # This uses AI/probabilistic logic (based on edit distance).
            suggestions = list(self.spell.candidates(word.lower()))

            if suggestions:
                # 7. Add each suggestion to the menu.
                # We use a lambda to capture the current value of 's'.
                for s in suggestions[:7]: # Show top 7 suggestions
                    self.suggestion_menu.add_command(
                        label=s,
                        command=lambda s=s: self.replace_word(word_start, word_end, s)
                    )
            else:
                self.suggestion_menu.add_command(label="No suggestions", state="disabled")

            # 8. Add "Add to Dictionary" option.
            self.suggestion_menu.add_separator()
            self.suggestion_menu.add_command(
                label="Add to Dictionary",
                command=lambda w=word: self.add_to_dict(w, word_start, word_end)
            )

            # 9. Post (display) the menu at the cursor's root coordinates.
            self.suggestion_menu.post(event.x_root, event.y_root)

    def replace_word(self, start, end, new_word):
        """
        Replaces the word in the given range with the new_word.
        """
        # 1. Delete the misspelled word.
        self.text_widget.delete(start, end)
        
        # 2. Insert the correct word.
        self.text_widget.insert(start, new_word)
        
        # 3. Re-run the spell check to clear the underline.
        self.check_spelling()

    def add_to_dict(self, word, start, end):
        """
        Adds a word to the spell checker's session dictionary and
        removes its "misspelled" tag.
        """
        # 1. Add the word (lowercase) to the dictionary for this session.
        self.spell.word_frequency.add(word.lower())
        
        # 2. Remove the tag from the specific word instance that was clicked.
        self.text_widget.tag_remove("misspelled", start, end)
        
        # 3. Re-run the full check to remove the tag from *all*
        #    instances of this word in the document.
        self.check_spelling()
        self.update_status(f"'{word}' added to session dictionary.")

    def on_close(self):
        """Handle the window closing event."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

def main():
    """
    Main function to create and run the application.
    """
    try:
        root = tk.Tk()
        app = SpellCheckerApp(root)
        root.mainloop()
    except ImportError:
        print("Error: 'pyspellchecker' library not found.")
        print("Please install it by running: pip install pyspellchecker")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()