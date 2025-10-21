import os
import csv
import requests

csv_file = "all_electronics.csv"
output_folder = r"C:\Users\AADITYA KHOPADE\Gainova Proj\images"
os.makedirs(output_folder, exist_ok=True)

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)
    for i, row in enumerate(reader, start=1):
        try:
            url = row[1].strip() 
            if not url:
                print(f"⚠️ Skipping row {i}: empty URL")
                continue
            file_name = f"img_{i:04d}.jpg"
            file_path = os.path.join(output_folder, file_name)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            with open(file_path, 'wb') as img_file:
                img_file.write(response.content)
            print(f"Downloaded {file_name}")
        except Exception as e:
            print(f"Failed to download row {i}: {e}")
print(f"\n🎯 Done! Images saved in: {output_folder}")