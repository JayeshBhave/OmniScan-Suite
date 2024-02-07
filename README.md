# Omniscan: Port Scanner and Directory Brute-forcer

Omniscan is a Python tool that provides functionalities for both port scanning and directory brute-forcing with threading support. It can be useful for network administrators and security professionals to identify open ports and discover potentially vulnerable directories on web servers.

## Features

- **Port Scanning**: Scan ports on a specified IP address or URL to identify open ports and corresponding service names.
- **Directory Brute-forcing**: Brute-force directories on a web server using a provided wordlist to discover hidden or sensitive directories.

## Installation

To install Omniscan system-wide, follow these steps:

### Requirements

- Python 3.x
- Requests library (install via `pip install requests`)

### Installation Steps

1. Clone the repository or download the `omniscan.py` file.

2. Open a terminal and navigate to the directory containing `omniscan.py`.

3. Run the following command to install Omniscan:

```bash
sudo make install
```
## Usage
### Basic Usage

To use Omniscan, execute the omniscan.py script with appropriate command-line arguments.

```bash
omniscan.py <target> [options]
```
Replace <target> with the IP address or URL of the target.
Options

    --port-scan: Perform port scanning.
    --dir-brute: Perform directory brute-forcing.
    -w, --wordlist <path>: Path to the directory wordlist.
    -t, --threads <num>: Number of threads to use (default: 4).

## Examples
Perform Port Scanning (Use IP address as Target)

```bash
omniscan.py 127.0.0.1 --port-scan
```
Perform Directory Brute-forcing (Use URL as Target)

```bash
omniscan.py example.com --dir-brute -w wordlist.txt
```
Replace wordlist.txt with the path to your directory wordlist file.
You can also use wordlist given in this repository.
## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or create a pull request on GitHub.