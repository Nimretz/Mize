import sys
import subprocess
import concurrent.futures

#enter domain list, output file name and word to search in each output
def run_whois(domain, grep_word):
    try:
        whois_output = subprocess.check_output(['whois', '-H', domain], stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError:
        return domain, 0

    matched_lines = [line for line in whois_output.split('\n') if grep_word.lower() in line.lower()]
    num_matched_lines = len(matched_lines)
    return f"{num_matched_lines:02}.{domain}", str(num_matched_lines)


if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    grep_word = sys.argv[3]

    with open(input_file) as f:
        domains = f.read().splitlines()

    with open(output_file, 'w') as f:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(run_whois, domain, grep_word) for domain in domains]
            for future in concurrent.futures.as_completed(futures):
                domain, result = future.result()
                f.write(f'{domain}\n')
                f.write(str(result))
                f.write('\n')

    print(f'Output saved to {output_file}')
                                           
