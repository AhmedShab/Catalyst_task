import sys
import csv
import MySQLdb
import optparse
import re

def insert_into_table(user_data):
    return None

def remove_invalidate_emails(data):
    is_valid = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if (is_valid.search(data["email"]) == None):
        del data["email"]
        return None

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
		data = csv.DictReader(csvfile)
		for row in data:
			try:
				row["email"] = row.pop("email\t")
				remove_invalidate_emails(row)
				# call insert_into_table with a valid email
				# insert_into_table(row)
				print(row["name"], row["surname"], row["email"])

			except Exception as e:
				print "the email is invalid! Please use a valid email"
				# no insertion happens
				continue

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
