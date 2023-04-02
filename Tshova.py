import argparse
import threading
import subprocess
from collections import defaultdict
#formerly known as malshin.py
#returns A and NS records from file containing list of domains (together ANS [answer])
def run_dig(domain, results):
    a_records = []
    ns_records = []

    try:
        # Run dig command to get A records
        a_output = subprocess.check_output(['dig', '+short', 'A', domain])
        a_records = a_output.decode().splitlines()

        # Run dig command to get NS records
        ns_output = subprocess.check_output(['dig', '+short', 'NS', domain])
        ns_records = ns_output.decode().splitlines()
    except subprocess.CalledProcessError as e:
        print(f'Error running dig for domain {domain}: {e}')

    # Add the result to the shared dictionary
    results[domain] = (a_records, ns_records)


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('output_file', help='Path to the output file')
    args = parser.parse_args()

    # Read the input file
    with open(args.input_file, 'r') as f:
        domains = [line.strip() for line in f]

    # Create a shared dictionary to hold the results
    results = {}

    # Create a list of threads
    threads = []
    for domain in domains:
        thread = threading.Thread(target=run_dig, args=(domain, results))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Group the domains by IP address
    ip_to_domains = defaultdict(list)
    for domain, (a_records, ns_records) in results.items():
        if not a_records or not ns_records:
            ip_to_domains['ERROR'].append(domain)
            continue

        ips = set(a_records)
        if len(ips) == 1:
            ip = ips.pop()
            ip_to_domains[ip].append(domain)
        else:
            # Check if both IP addresses are registered to the domain
            is_valid = all(ip in a_records for ip in ips)
            if is_valid:
                for ip in ips:
                    ip_to_domains[ip].append(domain)
            else:
                ip_to_domains['ERROR'].append(domain)

    # Write the results to the output file
    with open(args.output_file, 'w') as f:
        for ip, domains in ip_to_domains.items():
            if ip == 'ERROR':
                f.write('ERROR: No A or NS records found\n')
            else:
                count = len(domains)
                f.write(f'{ip} ({count} domains)\n')
                for domain in domains:
                    f.write(f'\t{domain}\n')


if __name__ == '__main__':
    main()
