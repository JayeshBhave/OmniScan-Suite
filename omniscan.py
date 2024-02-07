#!/usr/bin/env python3
import socket
import requests
import threading
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

# Global variables for thread synchronization
checked_directories = 0
total_directories = 0
lock = threading.Lock()

def port_scan(ip, max_workers=50):
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures_list = []
        for port in range(1, 65536):
            futures_list.append(executor.submit(scan_port, ip, port))
        for future in as_completed(futures_list):
            port, result = future.result()
            if result:
                service_name = get_service_name(port)
                open_ports.append((port, service_name))
    return open_ports

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.2)
            result = sock.connect_ex((ip, port))
            return port, result == 0
    except Exception as e:
        return port, False

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "Unknown"

def explore_directories(base_url, directory_list, thread_id, num_threads):
    global checked_directories

    for i in range(len(directory_list)):
        if i % num_threads == thread_id:  # Distribute directories among threads
            directory = directory_list[i]
            url = f"{base_url}/{directory}"
            response = requests.head(url)

            with lock:
                checked_directories += 1
                sys.stdout.write(f"\033[KThread-{thread_id}: Currently checking {directory}. Total Checked: {checked_directories}/{total_directories}\r")
                sys.stdout.flush()

            if response.status_code != 404:
                print(f"Found directory: {url} Status: {response.status_code} :")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Port Scanner and Directory Brute-forcer with threading')
    parser.add_argument('target', type=str, help='Target IP address or URL')
    parser.add_argument('--port-scan', action='store_true', help='Perform port scanning')
    parser.add_argument('--dir-brute', action='store_true', help='Perform directory brute-forcing')
    parser.add_argument('-w', '--wordlist', type=str, help='Path to directory wordlist')
    parser.add_argument('-t', '--threads', type=int, default=4, help='Number of threads (default: 4)')
    args = parser.parse_args()

    target = args.target
    wordlist = args.wordlist
    num_threads = args.threads

    if args.port_scan:
        parsed_url = urlparse(target)
        target_ip = socket.gethostbyname(parsed_url.netloc)
        open_ports = port_scan(target_ip, max_workers=num_threads)
        for port, service_name in open_ports:
            print(f"Port {port} ({service_name}) is open")

    if args.dir_brute and wordlist:
        with open(wordlist) as file:
            directories = file.read().splitlines()

        total_directories = len(directories)

        threads = []
        for i in range(num_threads):
            thread = threading.Thread(target=explore_directories, args=(target, directories, i, num_threads))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    elif args.dir_brute and not wordlist:
        print("Error: Directory wordlist is required for directory brute-forcing.")
