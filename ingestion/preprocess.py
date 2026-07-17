import uuid

from utils import (clean_text, extract_keywords, read_docx_file, write_to_csv,
                    write_to_jsonl)


def pre_process_documents(
    input_file: str, output_file: str, is_csv: bool = True, is_json: bool = True
):
    """
    Pre-processes the input document by performing section-based chunking and keyword extraction.
        Args:   input_file (str): Path to the input document file (.docx).
                output_file (str): Base path for the output file (without extension).
                is_csv (bool): Whether to write the output in CSV format.
                is_json (bool): Whether to write the output in JSONL format.
     Returns:        None
     Output:        Writes the processed data to a CSV and/or JSONL file based on the specified flags.
     The function reads a .docx file, extracts sections and subsections based on markdown-like headers (## for sections and ### for subsections), cleans the text, extracts keywords, and writes the processed data to the specified output files.
    """
    rows = []
    current_section = ""
    current_subsection = ""

    lines = read_docx_file(input_file=input_file)

    file_name = input_file.split("/")[-1].replace(".docx", "")

    buffer = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("## "):
            if buffer:
                rows.append(
                    {
                        "id": str(uuid.uuid4()),
                        "section": current_section,
                        "subsection": current_subsection,
                        "chunk": buffer.strip(),
                        "keywords": ",".join(extract_keywords(buffer.strip())),
                        "input_file": file_name,
                    }
                )

            buffer = ""
            current_section = line.replace("## ", "")
            current_subsection = "Definition"
            continue

        if line.startswith("### "):

            if buffer:
                rows.append(
                    {
                        "id": str(uuid.uuid4()),
                        "section": current_section,
                        "subsection": current_subsection,
                        "chunk": buffer.strip(),
                        "keywords": ",".join(extract_keywords(buffer.strip())),
                        "input_file": file_name,
                    }
                )

            buffer = ""
            current_subsection = line.replace("### ", "")
            continue

        buffer += " " + clean_text(line)

    # final flush
    if buffer:
        rows.append(
            {
                "id": str(uuid.uuid4()),
                "section": current_section,
                "subsection": current_subsection,
                "chunk": buffer.strip(),
                "keywords": ",".join(extract_keywords(buffer.strip())),
                "input_file": file_name,
            }
        )

    if is_csv:
        write_to_csv(rows=rows, output_file=output_file + ".csv")
    if is_json:
        write_to_jsonl(rows=rows, output_file=output_file + ".jsonl")
    print("RAG preprocessing completed")
