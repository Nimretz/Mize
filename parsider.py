import ipaddress
import sys

def get_valid_addresses(cidr_block):
    # Create an IP network object from the CIDR block string
    network = ipaddress.ip_network(cidr_block)

    # Iterate through all valid host addresses in the network
    valid_addresses = []
    for host in network.hosts():
        valid_addresses.append(str(host))

    return valid_addresses

if len(sys.argv) != 3:
    print("Usage: python cidr_parser.py input_file output_file")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file) as f:
    cidr_blocks = f.readlines()

with open(output_file, 'w') as f:
    for cidr_block in cidr_blocks:
        cidr_block = cidr_block.strip() # remove newline character
        valid_addresses = get_valid_addresses(cidr_block)
        for ip_address in valid_addresses:
            f.write(ip_address + "\n") # write each IP address in a new row
