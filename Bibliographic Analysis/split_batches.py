import csv
import os
import math

BASE_DIR = "/mnt/c/Users/DEll/Desktop/Master IT/S4/PFE/Articals/My Artical/Bibliographic Analysis"
MASTER = os.path.join(BASE_DIR, "master_unique_papers.csv")
BATCH_DIR = os.path.join(BASE_DIR, "batches")
os.makedirs(BATCH_DIR, exist_ok=True)

BATCH_SIZE = 100

# Read master file
with open(MASTER, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

total = len(rows)
num_batches = math.ceil(total / BATCH_SIZE)
print(f"Total papers: {total}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Number of batches: {num_batches}")

# Split into batches
for i in range(num_batches):
    start = i * BATCH_SIZE
    end = min(start + BATCH_SIZE, total)
    batch_rows = rows[start:end]
    
    batch_path = os.path.join(BATCH_DIR, f"batch_{i+1:02d}.csv")
    with open(batch_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(batch_rows)
    
    print(f"  Batch {i+1:02d}: papers {start+1}-{end} ({len(batch_rows)} rows) -> {os.path.basename(batch_path)}")

print(f"\nDone. {num_batches} batch files created in {BATCH_DIR}")
