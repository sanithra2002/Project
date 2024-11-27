import os
import time
import sys
import threading
import subprocess
import random
from pyudev import Context, Monitor, MonitorObserver
import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize Colorama for cross-platform compatibility


# Utilities for Cyberpunk UI
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def typing_print(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def animate_option(num, name, desc):
    CYBER_GREEN = "\033[38;2;0;255;128m"
    CYBER_PINK = "\033[38;2;255;20;147m"
    CYBER_BLUE = "\033[38;2;0;255;255m"
    RESET = "\033[0m"
    option_text = f"{CYBER_GREEN}{num}{RESET} {CYBER_PINK}{name}{RESET} - {CYBER_BLUE}{desc}{RESET}"
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
    animation = ["[□□□□□□□□□□]", "[■□□□□□□□□□]", "[■■□□□□□□□□]", "[■■■□□□□□□□]",
                 "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]",
                 "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
    start_time = time.time()
    while time.time() - start_time < duration:
        for frame in animation:
            print(f"\033[38;2;0;255;255m{frame} LOADING OPTIONS", end='\r', flush=True)
            time.sleep(0.1)
    print("\033[F\033[K", end='')

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
# USB Scanner
def on_device_event(device):
    if device.action == 'add' and device.get('ID_FS_TYPE') in ['vfat', 'ntfs', 'exfat', 'ext4']:
        dev_path = device.get('DEVNAME')
        scan_device(dev_path)


def scan_device(dev_path):
    command = ['sudo', 'clamscan', '-r', '--remove', dev_path]
    log_file_path = os.path.join(dev_path, 'clamscan_log.txt')
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
        with open(log_file_path, 'a') as log_file:
            log_file.write(result.stdout)
        print(f"Scan Completed! Log saved to {log_file_path}.")
    except Exception as e:
        print(f"Error: {str(e)}")


def usb_scanner():
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')
    observer = MonitorObserver(monitor, callback=on_device_event, name='observer')
    observer.start()
    typing_print("Monitoring USB ports. Plug in a USB device to test...", 0.05)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()


# System Scanner
def system_scanner():
    print("Preparing for system scan...")
    target_ip = input("Enter the target IP address: ").strip()
    if input("Are you sure you want to proceed? (y/n): ").lower() == 'y':
        subprocess.run(['nmap', '-sS', '-sV', '-O', target_ip])
        subprocess.run(['nmap', '--script', 'vuln', target_ip])


# Fuzzer
def find_directories(base_url, wordlist_file):
    found_dirs = []
    unfound_dirs = []
    with open(wordlist_file, 'r') as file:
        directories = file.read().splitlines()
    for directory in directories:
        url = f"{base_url}/{directory}/"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                found_dirs.append(url)
            elif response.status_code == 403:
                found_dirs.append(url)
            else:
                unfound_dirs.append(url)
        except requests.exceptions.RequestException:
            pass
    print(f"Found directories: {found_dirs}")
    print(f"Not found directories: {unfound_dirs}")


def fuzzer():
    base_url = input("Enter the website URL: ").strip()
    wordlist_file = "common.txt"
    find_directories(base_url, wordlist_file)


# Main Menu
def options_menu():
    while True:
        clear_screen()
        print("\033[38;2;255;20;147m\n╔═══════════════════════════╗")
        print("\033[38;2;255;20;147m║      SYSTEM OPTIONS       ║")
        print("\033[38;2;255;20;147m╚═══════════════════════════╝")
        options = [
            ("[1]", "USB Scanner", "Scan connected USB devices"),
            ("[2]", "System Scanner", "Scan system vulnerabilities"),
            ("[3]", "URL Fuzzer", "Discover hidden endpoints"),
            ("[4]", "Exit", "Terminate program")
        ]
        for num, name, desc in options:
            animate_option(num, name, desc)
        choice = input("\n[INPUT] Enter your choice (1-4): ").strip()
        if choice == "1":
            usb_scanner()
        elif choice == "2":
            system_scanner()
        elif choice == "3":
            fuzzer()
        elif choice == "4":
            typing_print("\033[38;2;255;0;0mSystem terminated. Goodbye!", 0.05)
            break
        else:
            print("\033[38;2;255;0;0mInvalid option! Please try again.\033[0m")



def main():
    clear_screen()
    port_scanning_art()
    loading_animation()
    clear_screen()
    typing_print("\033[38;2;0;0;255mWelcome to the Advanced Security Suite v1.0\033[0m", 0.05)
    time.sleep(1)
    options_menu()


if __name__ == "__main__":
    main()
