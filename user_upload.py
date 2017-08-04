import sys
import csv
import MySQLdb



with open(sys.argv[1], 'rb') as csvfile:
    filename = csv.reader(csvfile)
    for row in filename:
        print(row)
