import csv
import os

def query_csv(file_path):
    file_path = file_path.strip().strip('"').strip("'")

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    results = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        print(f"🔍 CSV Columns found: {reader.fieldnames}")

        required_columns = {'name', 'category', 'bio', 'email'}
        if not required_columns.issubset(set([col.strip() for col in reader.fieldnames])):
            print(f"❌ CSV must contain columns: {required_columns}")
            return

        for row in reader:
            category = row['category'].lower()
            bio = row['bio'].lower()

            has_hr = 'hr' in category or 'human resources' in category or \
                     'hr' in bio or 'human resources' in bio

            has_ny = 'ny' in category or 'nyc' in category or 'new york' in category or \
                     'ny' in bio or 'nyc' in bio or 'new york' in bio

            if has_hr and has_ny:
                results.append({
                    'Name': row['name'].strip(),
                    'Location': 'NY/NYC/New York',
                    'Email': row['email'].strip(),
                    'HR_Match': 'Human Resources'
                })

    if results:
        print(f"{'Name':<25} {'Location':<15} {'Email':<35} {'HR_Match'}")
        print("-" * 90)
        for r in results:
            print(f"{r['Name']:<25} {r['Location']:<15} {r['Email']:<35} {r['HR_Match']}")
    else:
        print("No matching records found.")

if __name__ == "__main__":
    csv_file_path = input("Enter the path to your CSV file: ").strip().strip('"').strip("'")
    query_csv(csv_file_path)
