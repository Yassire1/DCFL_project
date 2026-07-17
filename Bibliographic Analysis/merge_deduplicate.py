import csv
import os
import glob
from collections import defaultdict

BASE_DIR = "/mnt/c/Users/DEll/Desktop/Master IT/S4/PFE/Articals/My Artical/Bibliographic Analysis"

# Find all CSV files
csv_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.csv")))
# Exclude our own output files
csv_files = [f for f in csv_files if os.path.basename(f) not in 
             ['master_unique_papers.csv', 'merge_deduplicate.py']]

print(f"Found {len(csv_files)} CSV files")

# Read all papers: keyed by 'Key'
papers = {}  # Key -> {row_data, source_files, abstract_len}
header = None

for fpath in csv_files:
    fname = os.path.basename(fpath)
    print(f"  Reading: {fname}")
    with open(fpath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        file_header = next(reader)
        if header is None:
            header = file_header
        
        row_count = 0
        for row in reader:
            row_count += 1
            if len(row) < len(file_header):
                # Pad short rows
                row.extend([''] * (len(file_header) - len(row)))
            
            # Build dict from row
            row_dict = dict(zip(file_header, row))
            key = row_dict.get('Key', '').strip()
            
            if not key:
                continue
            
            abstract = row_dict.get('Abstract Note', '')
            abstract_len = len(abstract)
            
            if key not in papers:
                papers[key] = {
                    'row': row_dict,
                    'source_files': [fname],
                    'abstract_len': abstract_len
                }
            else:
                papers[key]['source_files'].append(fname)
                # Keep the record with the longest abstract
                if abstract_len > papers[key]['abstract_len']:
                    papers[key]['row'] = row_dict
                    papers[key]['abstract_len'] = abstract_len
        
        print(f"    Rows: {row_count}")

print(f"\nTotal unique papers: {len(papers)}")
total_with_dups = sum(len(p['source_files']) for p in papers.values())
print(f"Total rows (with duplicates): {total_with_dups}")
print(f"Duplicates merged: {total_with_dups - len(papers)}")
print(f"Papers appearing in multiple files: {sum(1 for p in papers.values() if len(p['source_files']) > 1)}")

# Add source tracking columns
header_out = header + ['__source_files__', '__source_count__']

# Save master file
output_path = os.path.join(BASE_DIR, "master_unique_papers.csv")
with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header_out)
    for key, data in papers.items():
        row = [data['row'].get(col, '') for col in header]
        row.append('; '.join(data['source_files']))
        row.append(str(len(data['source_files'])))
        writer.writerow(row)

print(f"\nSaved: {output_path}")

# Also save a mapping of Key -> source files for reference
mapping_path = os.path.join(BASE_DIR, "paper_source_mapping.csv")
with open(mapping_path, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Key', 'Title', 'Source_Files', 'Source_Count'])
    for key, data in papers.items():
        writer.writerow([
            key,
            data['row'].get('Title', ''),
            '; '.join(data['source_files']),
            str(len(data['source_files']))
        ])

print(f"Saved source mapping: {mapping_path}")
