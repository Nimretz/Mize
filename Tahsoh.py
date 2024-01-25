import sys
#remove contents of file1 in file2 - removing lines in file2 that are in file1, to remove sites that are not relevant from the scope
def compare_and_save(file1, file2, output_file):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines_to_remove = set(line.strip() for line in f1)

        removed_lines = []
        with open(output_file, 'w') as output:
            for line in f2:
                stripped_line = line.strip()
                if stripped_line in lines_to_remove:
                    removed_lines.append(stripped_line)
                else:
                    output.write(line)

        return removed_lines

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Tahsoh.py file1 file2 output_file")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output_file = sys.argv[3]

    removed_lines = compare_and_save(file1, file2, output_file)

    print("Comparison complete. Removed", len(removed_lines), "lines:")
    for removed_line in removed_lines:
        print("-", removed_line)

    print("Output saved to", output_file)
