#!/usr/bin/env python3
"""
remove_pdf_links.py

A command‐line tool to strip all hyperlink/hover actions (including /Annots, /OpenAction, /AA)
from PDFs, using pikepdf (which wraps qpdf for low‐level PDF editing).

Usage:
    python remove_pdf_links.py -i <input_path> -o <output_path>

Parameters:
    -i, --input:   Path to a single PDF file or a directory containing PDFs.
    -o, --output:  Path to a single PDF file (if input is one file)
                   or a directory where cleaned PDFs will be saved (if input is a directory).
"""

import os
import argparse
import pikepdf

def strip_links_from_pdf(input_pdf_path: str, output_pdf_path: str):
    """
    Open input_pdf_path, remove any /Annots, /OpenAction, /AA from each page
    and from the document catalog, then save to output_pdf_path.
    """
    pdf = pikepdf.Pdf.open(input_pdf_path)

    # 1) Iterate through every page and delete unwanted keys
    for page in pdf.pages:
        obj = page.obj
        if "/Annots" in obj:
            del obj["/Annots"]
        if "/OpenAction" in obj:
            del obj["/OpenAction"]
        if "/AA" in obj:
            del obj["/AA"]

    # 2) Remove any /OpenAction or /AA in the document catalog (root)
    root = pdf.trailer["/Root"]
    if "/OpenAction" in root:
        del root["/OpenAction"]
    if "/AA" in root:
        del root["/AA"]

    # 3) Save the cleaned PDF
    pdf.save(output_pdf_path)
    pdf.close()

def process_file(input_file: str, output_file: str):
    strip_links_from_pdf(input_file, output_file)
    print(f"Processed: {input_file} -> {output_file}")

def process_directory(input_dir: str, output_dir: str):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            cleaned_filename = os.path.splitext(filename)[0] + "_cleaned.pdf"
            output_path = os.path.join(output_dir, cleaned_filename)
            strip_links_from_pdf(input_path, output_path)
            print(f"Processed: {input_path} -> {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Strip all hyperlinks/hover actions from PDFs (using pikepdf).")
    parser.add_argument('-i', '--input', required=True,
                        help="Path to a PDF file or directory containing PDFs.")
    parser.add_argument('-o', '--output', required=True,
                        help="Path to a single PDF file (if input is a file) or an output directory.")

    args = parser.parse_args()
    input_path = args.input
    output_path = args.output

    if os.path.isfile(input_path):
        # Input is a single PDF file
        if os.path.isdir(output_path):
            # If output_path is a directory, construct a filename inside it
            cleaned_name = os.path.splitext(os.path.basename(input_path))[0] + "_cleaned.pdf"
            final_output = os.path.join(output_path, cleaned_name)
        else:
            final_output = output_path
        process_file(input_path, final_output)

    elif os.path.isdir(input_path):
        # Input is a directory of PDFs: output_path must be a directory
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        process_directory(input_path, output_path)

    else:
        print(f"Error: Input path '{input_path}' does not exist or is not a file/directory.")

if __name__ == "__main__":
    main()
