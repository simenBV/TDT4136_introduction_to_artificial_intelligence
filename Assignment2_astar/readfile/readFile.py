import os

samfArray = []

file = open("samfMap.txt", 'r')

for line in file.readlines():
    samfArray.append(line.split(','))

print(samfArray)
