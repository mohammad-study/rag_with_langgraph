import os
from pathlib import Path

from preprocess import pre_process_documents
from config import config, abs_path

raw_folder = abs_path(config["ingestion"]["raw_folder"])
process_folder = abs_path(config["ingestion"]["process_folder"])

if not os.path.exists(process_folder):
    os.makedirs(process_folder)


def main():
    """
    Main function to process documents in the raw folder and save the processed output in the process folder.
    The function iterates through all .docx files in the raw folder, processes each document
    """
    for file in os.listdir(raw_folder):

        if file.endswith(".docx"):
            input_path = os.path.join(raw_folder, file)
            output_file = os.path.join(process_folder, file.replace(".docx", ""))

            print(f"Processing {input_path}...")

            # Recursive chunking and keyword extraction
            pre_process_documents(
                input_file=input_path,
                output_file=output_file,
                is_csv=True,
                is_json=False,
            )


if __name__ == "__main__":
    main()
