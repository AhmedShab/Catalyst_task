import sys
import csv
import MySQLdb

create_table = "--create_table"
upload_file = "--file"

if sys.argv[1] == upload_file:
    with open(sys.argv[2], 'rb') as csvfile:
        filename = csv.reader(csvfile)
        for row in filename:
            print(row)

if sys.argv[1] == create_table:
    print(create_table)
