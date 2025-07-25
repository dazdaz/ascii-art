#!/usr/bin/env python3

import sys
import os
import time

def main():
    """
    This is the main function that runs our Amiga-style demo.
    It sets up the initial parameters, handles the animation loop,
    and ensures a clean exit when the user stops the script.
    """
    # --------------------------------------------------------------------------
    # ---[ DEMO SETUP ]---------------------------------------------------------
    # --------------------------------------------------------------------------

    # This is our masterpiece, the ASCII art logo. It's a list where each
    # item is a line of the logo. Using block characters gives it a nice
    # retro, chunky feel.
    logo = [
        "  ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗ ",
        " ██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║ ",
        " ██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║ ",
        " ██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║ ",
        " ╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║ ",
        "  ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝ ",
    ]
    logo_width = len(logo[0])
    logo_height = len(logo)

    # The classic scrolling message at the bottom of the screen.
    # We repeat it three times to ensure it loops smoothly and appears endless.
    scrolltext = (
        "   *** GREETINGS FROM GEMINI! THIS IS A PYTHON ASCII DEMO "
        "INSPIRED BY THE CLASSIC AMIGA SCENE OF THE LATE 80S AND EARLY 90S. "
        "KEEP THE OLD SCHOOL SPIRIT ALIVE! ***"
    ) * 3
    scroll_pos = 0

    # These are ANSI escape codes. They are special sequences of characters
    # that your terminal interprets as commands, like 'change color to red'.
    # We define them here to make the code cleaner and more readable.
    colors = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
    }
    # We will cycle through this list of colors to animate our logo.
    color_cycle = [colors['cyan'], colors['magenta'], colors['yellow'], colors['green'], colors['red']]
    color_index = 0

    # This controls the speed of our animation. 10 frames per second is a
    # good, smooth speed for a terminal demo.
    frame_delay = 1.0 / 10.0

    # --------------------------------------------------------------------------
    # ---[ MAIN LOOP ]----------------------------------------------------------
    # --------------------------------------------------------------------------

    # We wrap the main loop in a try...except block. This allows us to catch
    # the KeyboardInterrupt event (when the user presses Ctrl+C) and exit
    # gracefully, without leaving the terminal in a messy state.
    try:
        # Hide the blinking cursor to make the animation look cleaner.
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

        # This is the heart of the demo: an infinite loop that draws
        # each frame of the animation.
        while True:
            # --- GET TERMINAL SIZE ---
            # We get the terminal size in every frame. This makes our demo
            # responsive if the user resizes the window while it's running.
            try:
                # Attempt to get the current terminal size.
                term_width, term_height = os.get_terminal_size()
            except OSError:
                # If that fails (e.g., not running in a real terminal),
                # use a default fallback size.
                term_width, term_height = 80, 24

            # --- PREPARE THE FRAME ---
            # Instead of printing line by line (which can cause flickering),
            # we build the entire screen's content in a string buffer first.
            buffer = ""

            # This ANSI code moves the cursor to the top-left corner (1,1).
            buffer += "\033[H"

            # --- RENDER THE LOGO ---
            # Calculate the padding needed to center the logo on the screen.
            top_padding = (term_height - logo_height - 2) // 2
            left_padding_str = " " * ((term_width - logo_width) // 2)

            # Add the top padding (empty lines).
            if top_padding > 0:
                buffer += "\n" * top_padding

            # Get the current color for the logo from our color cycle.
            current_color = color_cycle[color_index]

            # Add each line of the logo to the buffer, with color codes.
            for i in range(logo_height):
                buffer += (
                    f"{left_padding_str}{current_color}"
                    f"{logo[i]}{colors['reset']}\n"
                )

            # --- RENDER THE SCROLLER ---
            # Fill the space between the logo and the scroller.
            fill_lines = term_height - top_padding - logo_height - 1
            if fill_lines > 0:
                buffer += "\n" * fill_lines

            # Create the visible portion of the scroller for this frame.
            # We add the start of the text to the end to make it loop smoothly.
            scroller_view = (scrolltext + scrolltext[:term_width])[scroll_pos:scroll_pos + term_width]

            # Add the scroller to the buffer.
            buffer += (
                f"{colors['bold']}{colors['yellow']}"
                f"{scroller_view.ljust(term_width)}"
                f"{colors['reset']}"
            )

            # --- DRAW THE FRAME ---
            # Now that the entire frame is in our buffer, we print it to the
            # screen all at once. flush() ensures it's displayed immediately.
            sys.stdout.write(buffer)
            sys.stdout.flush()

            # --- UPDATE STATE FOR NEXT FRAME ---
            # Move to the next color in the cycle.
            color_index = (color_index + 1) % len(color_cycle)
            # Advance the scroller text's position.
            scroll_pos = (scroll_pos + 1) % len(scrolltext)

            # Wait a short moment before drawing the next frame.
            time.sleep(frame_delay)

    except KeyboardInterrupt:
        # This part runs when the user presses Ctrl+C.
        print("\n\n>>> Demo finished. Stay creative! <<<\n")

    finally:
        # This code will run whether the demo exits normally or is
        # interrupted. It's crucial for cleaning up the terminal.
        # Show the cursor again.
        sys.stdout.write("\033[?25h")
        # Reset any colors or text styles.
        sys.stdout.write(colors['reset'])
        sys.stdout.flush()


if __name__ == "__main__":
    main()
