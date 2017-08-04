import sys
import csv
import MySQLdb
import optparse
import re

def append_quote_to_names(surname, single_quote):
	return surname[:1] + single_quote + surname[1:]

def contains_single_quote(surname, single_quote):
	return surname.find(single_quote) > -1


def insert_into_table(user_data, db):
	cursor = db.cursor()
	single_quote = "'"
	get_surname = user_data["surname"]
	surname = get_surname if not contains_single_quote(user_data["surname"], single_quote) else append_quote_to_names(get_surname, single_quote)

	sql = """
			insert into users(name, surname, email)
			values('{}', '{}', '{}')
		  """.format(user_data["name"],
		  			 surname,
					 user_data["email"])

	try:
		cursor.execute(sql)
		db.commit()

	except Exception as e:
		print "Database error"
		db.rollback()

	print "User data has been saved successfully"

def remove_invalid_email(data):
    if is_invalid_email(data["email"]):
        del data["email"]

def is_invalid_email(email):
	regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
	return regex.search(email) == None

def fix_fullname_format(fullname):
	if contains_non_alpha_chars(fullname):
		regex = re.compile("[^a-zA-Z]")
		fullname["name"] = regex.sub("", fullname["name"])
		fullname["surname"] = regex.sub("", fullname["surname"])

	capitalize_full_name(fullname)

def contains_non_alpha_chars(fullname):
	regex = re.compile("[.,\/#!$%\^&\*;:{}=\-_`~()]")
	return regex.search(fullname["name"]) is not None or regex.search(fullname["surname"]) is not None

def capitalize_full_name(fullname):
	fullname["name"] = fullname["name"].capitalize()
	fullname["surname"] = fullname["surname"].capitalize()

def remove_whitespaces(data):
	data["name"] = data["name"].strip()
	data["surname"] = data["surname"].strip()
	data["email"] = data["email"].strip()

def set_email_lower_case(emails):
	emails["email"] = emails["email"].lower()

def main():
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
					remove_invalid_email(row)
					fix_fullname_format(row)
					remove_whitespaces(row)
					set_email_lower_case(row)
					insert_into_table(row, db)

				except KeyError as e:
					print "The email is invalid! It won't be saved into the database. Please use a valid email"
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

main()
