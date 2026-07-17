import csv
import os
import json

BASE_DIR = "/mnt/c/Users/DEll/Desktop/Master IT/S4/PFE/Articals/My Artical/Bibliographic Analysis"
BATCH_DIR = os.path.join(BASE_DIR, "batches")
TASK_DIR = os.path.join(BASE_DIR, "screening_tasks")
os.makedirs(TASK_DIR, exist_ok=True)

batch_files = sorted([f for f in os.listdir(BATCH_DIR) if f.startswith("batch_")])

for bf in batch_files:
    batch_path = os.path.join(BATCH_DIR, bf)
    batch_num = bf.replace("batch_", "").replace(".csv", "")
    
    papers = []
    with open(batch_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            papers.append({
                "key": row.get("Key", ""),
                "title": row.get("Title", ""),
                "abstract": row.get("Abstract Note", ""),
                "year": row.get("Publication Year", ""),
                "tags_manual": row.get("Manual Tags", ""),
                "tags_auto": row.get("Automatic Tags", ""),
                "publication": row.get("Publication Title", "")
            })
    
    task_path = os.path.join(TASK_DIR, f"task_{batch_num}.json")
    with open(task_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    print(f"Task {batch_num}: {len(papers)} papers -> {os.path.basename(task_path)}")

print(f"\nDone. {len(batch_files)} task files created in {TASK_DIR}")
