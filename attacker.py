import time
import os
import sys
import random
import colorama
from colorama import Fore, Style


def clear_screen():
    """Clears the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typing_print(text, delay=0.05):
    """Simulates typing animation for text."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()  # Add a newline after the typing effect

def animate_option(num, name, desc):
    """Add animation for each option's display with cyberpunk colors."""
    # Cyberpunk-inspired colors using ANSI escape codes
    CYBER_GREEN = "\033[38;2;0;255;128m"  # Neon green
    CYBER_PINK = "\033[38;2;255;20;147m"  # Neon pink
    CYBER_BLUE = "\033[38;2;0;255;255m"   # Neon cyan
    RESET = "\033[0m"                     # Reset color

    # Assemble the styled string
    option_text = (
        f"{CYBER_GREEN}{num}{RESET} "  # Number in neon green
        f"{CYBER_PINK}{name}{RESET} - "  # Name in neon pink
        f"{CYBER_BLUE}{desc}{RESET}"  # Description in neon cyan
    )
    
    # Print with typing animation
    typing_print(option_text, 0.05)
def glitch_effect(text, repetitions=3):
    """Applies a glitch effect to the text."""
    glitch_chars = '!@#$%&'
    for _ in range(repetitions):
        glitched_text = ''.join(random.choice(glitch_chars) if random.random() < 0.1 else char for char in text)
        print(Fore.RED + glitched_text, end='\r')
        time.sleep(0.1)
    print(text)
def loading_animation(duration=3):
    """Displays a loading animation for the specified duration."""
    animation = [
        "[□□□□□□□□□□]",
        "[■□□□□□□□□□]",
        "[■■□□□□□□□□]",
        "[■■■□□□□□□□]",
        "[■■■■□□□□□□]",
        "[■■■■■□□□□□]",
        "[■■■■■■□□□□]",
        "[■■■■■■■□□□]",
        "[■■■■■■■■□□]",
        "[■■■■■■■■■□]",
        "[■■■■■■■■■■]"
    ]
    
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        print("\033[38;2;0;255;255m" + animation[i % len(animation)] + " LOADING OPTIONS", end='\r')
        time.sleep(0.1)
        i += 1
    print()  # Clear the loading animation line
    sys.stdout.write("\033[F\033[K")  # Move the cursor up and clear the line
def port_scanning_art():
    art = [
        "                                                                        ",
        "   _______              _    ______                                     ",
        "  |__   __|            | |  |  ____|                                    ",
        "     | | ___  _ __  ___| |_ | |__   _ __   __ _  __ _  __ _  ___        ",
        "     | |/ _ \\| '_ \\/ __| __||  __| | '_ \\ / _` |/ _` |/ _` |/ _ \\       ",
        "     | | (_) | | | \\__ \\ |_ | |____| | | | (_| | (_| | (_| |  __/      ",
        "     |_|\\___/|_| |_|___/\\__||______|_| |_|\\__, |\\__,_|\\__, |\\___|      ",
        "                                            __/ |       __/ |          ",
        "                                           |___/       |___/           ",
        "                                                                       "
    ]
    # Add glitch effect to the art
    for line in art:
        glitch_effect(Fore.CYAN + Style.BRIGHT + line)
        time.sleep(0.1)
def display_status(message, status="success"):
    """Displays a status message with cyberpunk color codes."""
    status_colors = {
        "success": "\033[38;2;0;255;128m",  # Neon green
        "warning": "\033[38;2;255;255;0m",  # Yellow
        "error": "\033[38;2;255;0;0m",      # Red
        "info": "\033[38;2;0;255;255m"      # Cyan
    }
    color = status_colors.get(status, "\033[0m")  # Default to reset
    print(f"\n{color}[{status.upper()}] {message}\033[0m")

def menu_loading_animation():
    """Displays an animation for loading menu options."""
    menu_title = "LOADING MENU OPTIONS..."
    for i in range(len(menu_title) + 1):
        sys.stdout.write("\033[38;2;0;255;0m" + menu_title[:i] + "\r")
        sys.stdout.flush()
        time.sleep(0.05)
    print()  # Move to the next line

def options_menu():
    """Displays the options menu with cyberpunk effects."""
    while True:
        menu_loading_animation()
        print("\033[38;2;255;20;147m\n╔═══════════════════════════╗")
        print("\033[38;2;255;20;147m║      SYSTEM OPTIONS       ║")
        print("\033[38;2;255;20;147m╚═══════════════════════════╝")
        
        options = [
            ("[ 1 ]", "Domain Checker", "Analyze domain security status"),
            ("[ 2 ]", "URL Fuzzer", "Discover hidden endpoints"),
            ("[ 3 ]", "System Scanner", "Scan system vulnerabilities"),
            ("[ 4 ]", "External Device Scanner", "Detect connected devices"),
            ("[ 5 ]", "Backdoor Detector", "Check for unauthorized access"),
            ("[ 6 ]", "Exit", "Terminate program")
        ]
        
        # Add animation for each menu option
        for num, name, desc in options:
            animate_option(num, name, desc)
        
        choice = input(f"\n\033[38;2;255;0;0m[INPUT] Enter your choice (1-6): \033[0m")
        
        if choice == "1":
            display_status("Initializing Domain Checker...", "info")
            loading_animation(2)
            display_status("Domain Checker activated", "success")
        elif choice == "2":
            display_status("Initializing URL Fuzzer...", "info")
            loading_animation(2)
            display_status("URL Fuzzer activated", "success")
        elif choice == "3":
            display_status("Initializing System Scanner...", "info")
            loading_animation(2)
            display_status("System Scanner activated", "success")
        elif choice == "4":
            display_status("Initializing External Device Scanner...", "info")
            loading_animation(2)
            display_status("External Device Scanner activated", "success")
        elif choice == "5":
            display_status("Initializing Backdoor Detector...", "info")
            loading_animation(2)
            display_status("Backdoor Detector activated", "success")
        elif choice == "6":
            display_status("Shutting down system...", "info")
            loading_animation(2)
            typing_print("\033[38;2;255;0;0mSystem terminated. Goodbye!\033[0m")
            break
        else:
            display_status("Invalid option selected", "error")

def main():
    """Main function to initialize the system."""
    clear_screen()
    loading_animation()
    clear_screen()
    port_scanning_art()
    typing_print("\033[38;2;0;0;255mWelcome to the Advanced Security Suite v1.0\033[0m", 0.05)
    time.sleep(1)
    options_menu()

if __name__ == "__main__":
    main()
