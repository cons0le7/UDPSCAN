import argparse
import socket
import sys

def color_red(text):
    RED = "\033[91m"
    RESET = "\033[0m"
    return f"{RED}{text}{RESET}"

def color_green(text):
    GREEN = "\033[32m"
    RESET = "\033[0m"
    return f"{GREEN}{text}{RESET}"

def print_banner():
    print(color_red("""  
________________________________________________________
  _    _ _____  _____     _____  _____          _   _ 
 | |  | |  __ \|  __ \   / ____|/ ____|   /\   | \ | |
 | |  | | |  | | |__) | | (___ | |       /  \  |  \| |
 | |  | | |  | |  ___/   \___ \| |      / /\ \ | . ` |
 | |__| | |__| | |       ____) | |____ / ____ \| |\  |
  \____/|_____/|_|      |_____/ \_____/_/    \_\_| \_|
--------------------------------------------------------
                     - v1.1.0 -
--------------------------------------------------------
 ------- https://github.com/cons0le7/UDPSCAN -------
         -----------------------------------
                ---------------------
                       -------
                                                      
 """))

def scan_udp_port(target_ip, port, timeout):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout) 
        message = b"Ping!"
        sock.sendto(message, (target_ip, port))
        try:
            response, addr = sock.recvfrom(1024)
            print(color_green(f"Port {port} is open."))
        except socket.timeout:
            print(color_red(f"Port {port} is closed or filtered."))
    except Exception as e:
        print(color_red(f"Error scanning port {port}: {e}"))
    finally:
        sock.close()

def parse_ports(ports_arg):
    ports = set()
    for part in ports_arg.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    return sorted(ports)

def scan(target_ip, ports_to_scan, timeout):
    for port in ports_to_scan:
        scan_udp_port(target_ip, port, timeout)

def main():
    print_banner()
    parser = argparse.ArgumentParser(
        description="UDP Port Scanner.",
        formatter_class=argparse.RawTextHelpFormatter, 
        epilog="""
  Syntax: 
  UDPSCAN.py -i/d [IP/DOMAIN] -p [PORTS] -t [TIMEOUT] 
  
  Examples:
  UDPSCAN.py -i 192.168.1.1 -p 123,5060
  UDPSCAN.py -d example.com -p 1-1024 -t 2
  UDPSCAN.py --ip 8.8.8.8 -p 53
  UDPSCAN.py --domain example.com --timeout 3
  UDPSCAN.py -i 192.168.1.2 --ports 53,67,68 

"""
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-i', '--ip', type=str, help='IP address to scan. (eg. 1.1.1.1)')
    group.add_argument('-d', '--domain', type=str, help='Domain name to scan. (eg. website.com)')    
    parser.add_argument('-p', '--ports', type=str, help='Ports to scan (single, multiple comma-separated or range).')
    parser.add_argument('-t', '--timeout', type=float, help='Timeout in seconds for each port scan (default is 1).')
    args = parser.parse_args()
    
    if args.ip or args.domain:
        target = args.ip or args.domain
        try:
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            print(color_red("Invalid hostname or IP address provided. Exiting."))
            sys.exit(1)

        ports_to_scan = args.ports and parse_ports(args.ports) or []
        if not ports_to_scan:
            print(color_red("No ports provided. Exiting."))
            sys.exit(1)

        timeout = args.timeout if args.timeout is not None else 1.0
        scan(target_ip, ports_to_scan, timeout)
    else:
        while True:
            target = input("Enter IP address or domain name to scan: ")
            try:
                target_ip = socket.gethostbyname(target)
            except socket.gaierror:
                print(color_red("Invalid hostname or IP address. Please try again."))
                continue

            ports_input = input("Enter ports to scan (single, comma-separated, or range): ")
            ports_to_scan = parse_ports(ports_input)
            timeout = input("Enter timeout in seconds for each port scan (default 1): ")
            timeout = float(timeout) if timeout else 1.0

            scan(target_ip, ports_to_scan, timeout)

            end_choice = input(color_green("Scan complete. New scan? (y/n): ").strip().lower())
            if end_choice != "y":
                break
main()