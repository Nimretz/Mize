import sys
import ipaddress

#Accepts list of IP addresses and sorts them back to CIDR

def group_ips_by_subnet(file_path):
    subnets = set()

    with open(file_path, 'r') as file:
        ip_addresses = file.read().splitlines()

    for ip_str in ip_addresses:
        ip_str = ip_str.strip()
        if not ip_str:
            continue  # Skip empty lines

        try:
            ip = ipaddress.ip_network(ip_str)
            subnet = ip.supernet(new_prefix=24)  # Adjust the prefix length as per your requirements
            subnets.add(str(subnet))
        except ValueError:
            print(f"Invalid IP address: {ip_str}")

    return '\n'.join(subnets)

# Example usage: python3 lama.py input.txt
if len(sys.argv) < 2:
    print("Please provide the path to the input file as a command-line argument.")
    sys.exit(1)

input_file = sys.argv[1]
cidr_list = group_ips_by_subnet(input_file)
print(cidr_list)
