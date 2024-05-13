import os
import re
import logging

# Configure logging to write to both file and console
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler('process_cpp_files.log'),
                        logging.StreamHandler()
                    ])

def find_cpp_files(directory):
    """ Walk through the directory and collect all .cpp files. """
    cpp_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.cpp'):
                cpp_files.append(os.path.join(root, file))
                logging.info(f"Found C++ file: {os.path.join(root, file)}")
    return cpp_files

def extract_strings_from_file(file_path):
    """ Extract all string literals from a single C++ file, applying advanced filters. """
    string_pattern = r'\"(.*?)\"'  # Regex to find anything inside quotes
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            strings = re.findall(string_pattern, file_content)
            filtered_strings = [
                s for s in strings 
                if s 
                and "###" not in s 
                and "##" not in s 
                and ".hpp" not in s 
                and ".h" not in s  # Skip strings containing ".h"
                and not (s.islower() and '_' in s)  # Skip lowercase strings with an underscore
                and not (s.islower() and not re.search(r'\s', s))  # Skip fully lowercase strings with no whitespace
            ]
            logging.info(f"Extracted {len(filtered_strings)} valid strings from {file_path}")
            return filtered_strings
    except Exception as e:
        logging.error(f"Failed to process {file_path}: {str(e)}")
        return []

def write_strings_to_ini(strings, output_file):
    """ Write the extracted strings to an INI file, using 'String=' format. """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for string in strings:
                file.write(f"{string}=\n")
            logging.info(f"Successfully wrote {len(strings)} strings to {output_file}")
    except Exception as e:
        logging.error(f"Failed to write to {output_file}: {str(e)}")

def main(directory, output_file):
    try:
        cpp_files = find_cpp_files(directory)
        all_strings = []
        for file in cpp_files:
            strings = extract_strings_from_file(file)
            all_strings.extend(strings)
        write_strings_to_ini(all_strings, output_file)
        logging.info("Finished processing all files.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main('FilePATH', 'output.ini')
