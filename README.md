# UDPSCAN
A Python based UDP port scanner developed for use with iSH Shell. This was taken from the [FLOOD](https://github.com/cons0le7/FLOOD) tool and modified to include command line parsed arguements for better flexibility and use with automation. It was isolated as a standalone tool due to being unable to use TCP raw sockets on iOS devices. 

**Note: As of now all the tool does is ping which is rather ineffective. I am currently working on specifically crafted packets targetting common services for specific ports and will update the tool once I find success in this**

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
This script can be ran in two ways: 

- You can run `python3 UDPSCAN.py` and you will be prompted to input ip/domain, ports and timeout in seconds.
- You can also run the script with arguements in command line. The syntax for this is
`python3 UDPSCAN.py -i/d [IP/DOMAIN] -p [PORTS] -t [TIMEOUT] `
- You will need to use `-i`, `--ip`, `-d`, or `--domain` to specify either a target ip address or domain name.
- You will need to use `-p` or `--ports` to specify ports. this can be a single port, multiple ports seperated by commas eg.`1,2,3` or a port range eg.`1-1024`
- The `-t` or `--timeout` arguement is optional, timeout is in seconds and if unused it will default to 1.
  
## Example Usage:

python3 UDPSCAN.py -i 192.168.1.1 -p 123,5060

python3 UDPSCAN.py -d example.com -p 1-1024 

python3 UDPSCAN.py --ip 8.8.8.8 -p 53

python3 UDPSCAN.py --domain example.com --timeout 2

python3 UDPSCAN.py -i 192.168.1.2 --ports 53,67,68 -t 3
