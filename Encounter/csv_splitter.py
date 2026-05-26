import pandas as pd
import os

def split_csv(input_filepath, rows_per_chunk, output_prefix="chunk_", output_dir="."):
    """
    Splits a large CSV file into multiple smaller CSV files.

    Args:
        input_filepath (str): The path to the large input CSV file.
        rows_per_chunk (int): The maximum number of rows for each output CSV file.
        output_prefix (str, optional): A prefix for the names of the output CSV files.
                                       Defaults to "chunk_".
        output_dir (str, optional): The directory where the split CSV files will be saved.
                                    Defaults to the current directory.
    """
    if not os.path.exists(input_filepath):
        print(f"Error: Input file '{input_filepath}' not found.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    print(f"Starting to split '{input_filepath}' into chunks of {rows_per_chunk} rows...")

    chunk_number = 1
    try:
        # Use pandas read_csv with chunksize to read the file in chunks
        # This is memory-efficient for very large files
        for chunk in pd.read_csv(input_filepath, chunksize=rows_per_chunk):
            output_filename = os.path.join(output_dir, f"{output_prefix}{chunk_number}.csv")
            chunk.to_csv(output_filename, index=False) # index=False prevents pandas from writing the DataFrame index as a column
            print(f"Created '{output_filename}' with {len(chunk)} rows.")
            chunk_number += 1
        print(f"Splitting complete. Total {chunk_number - 1} files created.")
    except Exception as e:
        print(f"An error occurred during splitting: {e}")

# --- How to use the function ---
if __name__ == "__main__":
    # Prompt the user for the input CSV file path
    input_csv_file = input("Please enter the full path to your large CSV file: ")

    # Set the desired number of rows per output CSV file.
    # Google Sheets has a 10 million cell limit, and often performs poorly above 100,000 rows.
    # A chunk size like 50,000 or 100,000 rows is usually a good starting point for Sheets.
    rows_per_output_file = 50000

    # Optional: Set a prefix for the output files (e.g., "my_data_part_1.csv")
    output_file_prefix = "my_data_part_"

    # Optional: Set a directory for the output files (e.g., "split_csv_files")
    # If not specified, files will be saved in the same directory as the script.
    output_directory = "split_csv_output"

    split_csv(input_csv_file, rows_per_output_file, output_file_prefix, output_directory)

    print("\nTo run this script:")
    print("1. Save the code above as a Python file (e.g., `csv_splitter.py`).")
    print("2. Make sure you have pandas installed: `pip install pandas`")
    print("3. Run the script from your terminal: `python csv_splitter.py`")
    print("4. When prompted, enter the full path to your large CSV file.")
    print("5. Adjust `rows_per_output_file` in the script if you want a different chunk size.")
    print(f"Your split CSV files will be saved in the '{output_directory}' directory.")
