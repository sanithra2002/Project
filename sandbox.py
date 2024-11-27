import tkinter as tk
from tkinter import ttk, scrolledtext, simpledialog
import threading
import time
import socket
from scapy.all import sniff
from scapy.layers.inet import IP, TCP, UDP
import psutil
from collections import defaultdict
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


# Network Traffic Monitoring Functions
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google's DNS server
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "127.0.0.1"


def display_packet(packet, text_widget):
    if IP in packet:
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        protocol = "TCP" if TCP in packet else "UDP" if UDP in packet else "Other"
        local_ip = get_local_ip()

        text_widget.insert(tk.END, "Source: ")
        text_widget.insert(tk.END, ip_src, "local_ip" if ip_src == local_ip else "external_ip")
        text_widget.insert(tk.END, " -> Destination: ")
        text_widget.insert(tk.END, ip_dst, "local_ip" if ip_dst == local_ip else "external_ip")
        text_widget.insert(tk.END, f" | Protocol: {protocol}\n")
        text_widget.see(tk.END)


def capture_traffic(text_widget):
    sniff(prn=lambda packet: display_packet(packet, text_widget), store=False)


def start_sniffing(text_widget):
    threading.Thread(target=capture_traffic, args=(text_widget,), daemon=True).start()


# Port Monitoring Functions
def get_open_ports():
    connections = psutil.net_connections(kind='inet')
    open_ports = defaultdict(list)
    for conn in connections:
        if conn.status in {psutil.CONN_LISTEN, psutil.CONN_ESTABLISHED}:
            open_ports[conn.laddr.port].append(conn.laddr.ip)
    return open_ports


def track_ports(interval, text_widget):
    previous_ports = get_open_ports()
    while True:
        current_ports = get_open_ports()
        newly_opened_ports = {port: current_ports[port] for port in current_ports if port not in previous_ports}
        newly_closed_ports = {port: previous_ports[port] for port in previous_ports if port not in current_ports}

        for port, ip in newly_opened_ports.items():
            text_widget.insert(tk.END, f"Port {port} opened on IP {ip}\n", "cyan")
        for port, ip in newly_closed_ports.items():
            text_widget.insert(tk.END, f"Port {port} closed on IP {ip}\n", "red")

        text_widget.see(tk.END)
        previous_ports = current_ports
        time.sleep(interval)


def start_port_tracking(interval, text_widget):
    threading.Thread(target=track_ports, args=(interval, text_widget), daemon=True).start()


# GUI Setup
def create_gui(selection):
    root = tk.Tk()
    root.title("Network & Port Monitoring")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    if selection in {"1", "3"}:
        # Network Traffic Tab
        network_tab = tk.Frame(notebook, bg="black")
        notebook.add(network_tab, text="Network Traffic")

        network_text = scrolledtext.ScrolledText(network_tab, wrap=tk.WORD, bg="black", fg="white", insertbackground="white")
        network_text.pack(expand=True, fill="both")
        network_text.tag_config("local_ip", foreground="green")
        network_text.tag_config("external_ip", foreground="red")
        start_sniffing(network_text)

    if selection in {"2", "3"}:
        # Port Monitoring Tab
        port_tab = tk.Frame(notebook, bg="black")
        notebook.add(port_tab, text="Port Monitoring")

        port_text = scrolledtext.ScrolledText(port_tab, wrap=tk.WORD, bg="black", fg="white", insertbackground="white")
        port_text.pack(expand=True, fill="both")
        port_text.tag_config("cyan", foreground="cyan")
        port_text.tag_config("red", foreground="red")
        start_port_tracking(2, port_text)

    root.mainloop()


def prompt_user():
    # Create a temporary Tkinter root for the input dialog
    input_root = tk.Tk()
    input_root.withdraw()  # Hide the root window

    # Ask the user for input
    user_choice = simpledialog.askstring(
        "User Input",
        "Select the monitoring tool:\n1. Network Traffic Monitoring\n2. Port Monitoring\n3. Both\nEnter your choice (1/2/3):"
    )

    # Validate user input
    if user_choice not in {"1", "2", "3"}:
        tk.messagebox.showerror("Error", "Invalid input! Please restart and enter 1, 2, or 3.")
        return None

    return user_choice


if __name__ == "__main__":
    # Prompt the user for their choice
    choice = prompt_user()

    if choice:
        create_gui(choice)