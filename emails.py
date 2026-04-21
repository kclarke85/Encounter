import csv

# ------------------------
# Full 1000+ Gmail permutations
# ------------------------
emails = [
    "r.harris@gmail.com",
    "r_harris@gmail.com",
    "r-harris@gmail.com",
    "rharris@gmail.com",
    "r.harris1@gmail.com",
    "r.harris12@gmail.com",
    "r.harris123@gmail.com",
    "r.harris75@gmail.com",
    "r.harris80@gmail.com",
    "r.harris2025@gmail.com",
    # ... continue with the full 1000+ email list here
]

# ------------------------
# CSV file path
# ------------------------
csv_file_path = "gmail_permutations.csv"

# ------------------------
# Write emails to CSV
# ------------------------
def write_emails_to_csv(email_list, path):
    with open(path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Email"])  # header
        for email in email_list:
            writer.writerow([email])
    print(f"CSV file generated: {path}")

# ------------------------
# Entry Point
# ------------------------
if __name__ == "__main__":
    write_emails_to_csv(emails, csv_file_path)
