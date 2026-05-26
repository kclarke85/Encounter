# import csv
# import os
# import dns.resolver
#
# def has_mx_record(domain):
#     """
#     Check if a domain has at least one MX record.
#     """
#     try:
#         answers = dns.resolver.resolve(domain, 'MX')
#         return len(answers) > 0
#     except:
#         return False
#
# def check_emails(file_path):
#     file_path = file_path.strip().strip('"').strip("'")
#
#     if not os.path.exists(file_path):
#         print(f"❌ File not found: {file_path}")
#         return
#
#     total_emails = 0
#     valid_domains = 0
#
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#
#         print(f"🔍 CSV Columns: {reader.fieldnames}")
#
#         if 'email' not in reader.fieldnames:
#             print("❌ CSV must contain a column named 'email'")
#             return
#
#         for row in reader:
#             email = row['email'].strip()
#             if '@' not in email:
#                 continue
#
#             domain = email.split('@')[-1].lower()
#             total_emails += 1
#
#             if has_mx_record(domain):
#                 valid_domains += 1
#
#     # if total_emails > 0:+
#         probability = (valid_domains / total_emails) * 100
#         print(f"\n✅ Emails checked: {total_emails}")
#         print(f"✅ Domains with MX record: {valid_domains}")
#         print(f"🎯 Probability of delivery (based on MX): {probability:.2f}%")
#     else:
#         print("❌ No valid emails found in the file.")
#
# if __name__ == "__main__":
#     csv_file_path = input("Enter the path to your CSV file: ").strip().strip('"').strip("'")
#     check_emails(csv_file_path)
