import csv

filepath = r"C:\Users\jonas\Desktop\TPA_Kolb\Oszilloskop Messungen 19.4.23\WA000001.CSV"

with open(filepath, 'r') as file:
    reader = csv.reader(file)
    
    lines = []
    
    for row in reader:
        lines.append(row)     


