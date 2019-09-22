import csv

csvfile = open("Samfundet_map_Edgar_full.csv","r")

reader = csv.reader(csvfile, delimiter=',', quotechar='|')

arr = []

for row in reader:
    arr.append(row)

print(arr)