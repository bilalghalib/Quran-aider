import os
import pyperclip

def export_and_copy_dart_files(source_folder, output_file):
    all_content = ""

    # Walk through the directory tree
    for root, dirs, files in os.walk(source_folder):
        for filename in files:
            if filename.endswith('.dart'):
                # Construct file path
                source_file = os.path.join(root, filename)

                # Read the source file
                with open(source_file, 'r') as file:
                    content = file.read()

                # Append content to the aggregate string
                all_content += f"// Title: {filename}\n\n{content}\n\n"

    # Write all content to the output file
    with open(output_file, 'w') as file:
        file.write(all_content)

    # Copy content to clipboard
    pyperclip.copy(all_content)
    print(f"All Dart files have been exported and copied to clipboard.")

# Usage
lib_folder = './lib/'  # Replace with the path to your 'lib' folder
output_file = './lib/output.txt'  # Replace with your desired output file path
export_and_copy_dart_files(lib_folder, output_file)
