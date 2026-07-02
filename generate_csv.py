import csv

with open("app/data/million.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["number"])

    for i in range(1, 1_000_001):
        writer.writerow([i])

print("Done")
