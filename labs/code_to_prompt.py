import argparse
import os


def code_to_prompt(folder_path, output_file="merged_code.py"):
    with open(output_file, "w") as outfile:
        outfile.write("This is the latest code:\n\n")
        outfile.write("```\n\n")
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)

                    # Write header with the file path
                    outfile.write(f"\n{'=' * 60}\n")
                    outfile.write(f"Full file path name: {file_path}\n")
                    outfile.write(f"{'=' * 60}\n\n")

                    # Write the content of the Python file
                    with open(file_path, "r") as infile:
                        outfile.write(infile.read())
                        outfile.write("\n\n")  # Add extra space after each file
        outfile.write("```\n\n")

    print(f"Merged code is saved in {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge all Python files in a folder.")
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing Python files."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="merged_code.py",
        help="Output file name for the merged code.",
    )

    args = parser.parse_args()

    code_to_prompt(args.folder_path, args.output)
