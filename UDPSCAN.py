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
    
    parser.add_argument('-p', '--ports', type=str, help='Ports to scan (single, multiple comma-separated \n(eg. 1,2,3) or range (eg. 1-1024)).')
    parser.add_argument('-t', '--timeout', type=float, help='Timeout in seconds for each port scan \n(default is 1).')

    args = parser.parse_args()

    target = args.ip or args.domain

    if not target:
        target = input("Enter IP address or domain name to scan: ")

    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(color_red("Invalid hostname or IP address."))
        sys.exit()

    ports_to_scan = []
    if args.ports:
        ports_to_scan = parse_ports(args.ports)
    if not ports_to_scan:
        ports_input = input("Enter ports to scan (single, comma separated or range): ")
        ports_to_scan = parse_ports(ports_input)

    if args.timeout is not None:
        timeout = args.timeout
    else:
        timeout = 1.0
        if not args.ports and args.ip is None and args.domain is None:
            user_timeout = input("Enter timeout in seconds (default 1): ")
            if user_timeout.strip():
                try:
                    timeout = float(user_timeout)
                    if timeout <= 0:
                        print(color_red("Timeout must be greater than 0. Defaulting to 1 second."))
                        timeout = 1.0
                except ValueError:
                    print(color_red("Invalid input. Defaulting to 1 second."))
                    timeout = 1.0

    for port in ports_to_scan:
        scan_udp_port(target_ip, port, timeout)

    print("Scan complete. Exiting...")
    sys.exit()

main()