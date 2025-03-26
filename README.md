# UDPSCAN
A Python based UDP port scanner developed for use with iSH Shell. This was taken from the [FLOOD](https://github.com/cons0le7/FLOOD) tool and modified to include command line parsed arguements for better flexibility and use with automation. It was isolated as a standalone tool due to being unable to use TCP raw sockets on iOS devices. 

![Image](https://github.com/user-attachments/assets/252fe3f9-800f-4853-bd56-b4e787014b28)

## Installation 
```
apk add git
apk add python3
git clone https://github.com/cons0le7/UDPSCAN
cd UDPSCAN
python3 UDPSCAN.py 
```

## Usage 

usage: UDPSCAN.py [-h] [-i IP | -d DOMAIN] [-p PORTS] [-t TIMEOUT]

UDP Port Scanner.

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP address to scan. (eg. 1.1.1.1)
  -d DOMAIN, --domain DOMAIN
                        Domain name to scan. (eg. website.com)
  -p PORTS, --ports PORTS
                        Ports to scan (single, multiple comma-separated 
                        (eg. 1,2,3) or range (eg. 1-1024)).
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout in seconds for each port scan 
                        (default is 1).

  Syntax: 
  UDPSCAN.py -i/d [IP/DOMAIN] -p [PORTS] -t [TIMEOUT] 
  
  Examples:
  UDPSCAN.py -i 192.168.1.1 -p 123,5060
  UDPSCAN.py -d example.com -p 1-1024 -t 2
  UDPSCAN.py --ip 8.8.8.8 -p 53
  UDPSCAN.py --domain example.com --timeout 3
  UDPSCAN.py -i 192.168.1.2 --ports 53,67,68 
