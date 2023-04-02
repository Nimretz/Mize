import argparse
import ipaddress

#run with a file containing CIDR (seperated by newline) as argument to print all IPs in the range
def get_ip_addresses(start_ip, end_ip):
    # Strip whitespace from start and end IP address strings
    start_ip = start_ip.strip()
    end_ip = end_ip.strip()

    # Convert the start and end IP addresses to IP objects
    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)

    # Iterate over the range of IP addresses
    ip_addresses = []
    for ip in range(int(start_ip), int(end_ip)+1):
        ip_addresses.append(str(ipaddress.IPv4Address(ip)))

    return ip_addresses

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Reads IP address ranges from a file and prints the IP addresses in each range.")
parser.add_argument("filename", help="The name of the file containing IP address ranges, one per line.")
args = parser.parse_args()

# Read IP address ranges from file and print IP addresses in each range
with open(args.filename, "r") as f:
    for line in f:
        start_ip, end_ip = line.strip().split("-")
        ip_addresses = get_ip_addresses(start_ip, end_ip)

        # Print IP range header
        print(start_ip + "-" + end_ip)

        # Print each IP address in range on a new line
        for ip_address in ip_addresses:
            print(ip_address)

        # Print blank line between ranges
        print()
