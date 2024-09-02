from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
import os

def clean_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(options: dict, selector: str = '>'):
    bindings = KeyBindings()
    global option_selector
    option_selector = 0

    @bindings.add('down')
    def go_down(event):
        global option_selector
        if option_selector < len(options) - 1:
            option_selector += 1
        refresh_display()

    @bindings.add('up')
    def go_up(event):
        global option_selector
        if option_selector > 0:
            option_selector -= 1
        refresh_display()

    @bindings.add('enter')
    def select_option(event):
        global option_selector
        selected_key = list(options.keys())[option_selector]
        function = options[selected_key]
        function()
        raise SystemExit

    def refresh_display():
        clean_screen()
        for idx, (key, value) in enumerate(options.items()):
            if idx == option_selector:
                print(f"{selector} {key}")
            else:
                print(f"  {key}")

    session = PromptSession(key_bindings=bindings)
    
    print("Use arrow keys to navigate, Enter to select.")
    refresh_display()
    
    while True:
        session.prompt()  # No prompt text needed, just to keep accepting input
