import sys
import csv
import MySQLdb
import optparse

create_table = "--create_table"
upload_file = "--file"

parser = optparse.OptionParser()

parser.add_option('--file',
                  action="store", type="string",
                  dest="file",help="require the csv file to insert the data into the users table")

parser.add_option('--create_table',
                  action="store_true", dest="create_table",
                  help="This will build/rebuild a new table")

parser.add_option('-u',
                  action="store", dest="username",
                  help="MySQL username")

parser.add_option('-p',
               action="store", dest="password",
               help="MySQL password")

parser.add_option('--host',
                  action="store", dest="host",
                  help="MySQL host")

(options, args) = parser.parse_args()

db = MySQLdb.connect(host=options.host, user=options.username, passwd=options.password, db="record")

cursor = db.cursor()

if options.file:
    with open(options.file, 'rb') as csvfile:
        filename = csv.reader(csvfile)
        for row in filename:
            print(row)

elif options.create_table:
        cursor.execute("drop table if exists users")
        sql = """create table users(
                name char(20),
                surname char(20),
                email char(30),
                unique (email)
                );"""
        cursor.execute(sql)

db.close()
