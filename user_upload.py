import sys
import csv
import MySQLdb
import optparse
import re
from MySQLdb import IntegrityError
from MySQLdb import ProgrammingError

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
		cursor.close()

	except IntegrityError as e:
		print "The email {} exists! Cannot save duplicate emails".format(user_data["email"])
		db.rollback()

	else:
		print "User data has been saved successfully"

def remove_invalid_email(data):
	email = data
	if is_invalid_email(email["email"]):
		del email["email"]

	return email["email"]


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

def capitalize_surname(surname):
	char_index = 2
	return surname.replace(surname[char_index], surname[char_index].capitalize())

def capitalize_full_name(fullname):
	fullname["name"] = fullname["name"].capitalize()
	fullname["surname"] = fullname["surname"].capitalize()

	if contains_single_quote(fullname["surname"], "'"):
		fullname["surname"] = capitalize_surname(fullname["surname"])

def remove_whitespaces(data):
	data["name"] = data["name"].strip()
	data["surname"] = data["surname"].strip()
	data["email"] = data["email"].strip()

def set_email_lower_case(emails):
	return emails["email"].lower()

def parse_csvfile(filename, db, include_table_insertion = True):
	cursor = db.cursor()

	with open(filename, 'rb') as csvfile:
		data = csv.DictReader(csvfile)

		for row in data:
			try:
				row["email"] = remove_invalid_email(row)
				fix_fullname_format(row)
				remove_whitespaces(row)
				row["email"] = set_email_lower_case(row)

				if include_table_insertion:
					insert_into_table(row, db)

			except KeyError as e:
				print "The email is invalid! It won't be saved into the database. Please use a valid email"
				continue

def create_table(db):
	cursor = db.cursor()

	try:
		cursor.execute("drop table if exists users")
		sql = """create table users(
				name char(20),
				surname char(20),
				email char(30),
				unique (email)
				);"""
		cursor.execute(sql)

	except ProgrammingError as e:
		print "Could not create a new table! You have a syntax error "

	else:
		cursor.close()
		print "Created the users table successfully"

def main():
	parser = optparse.OptionParser()

	parser.add_option('--file',
					action="store", type="string",
					dest="file",help="Require the csv file to insert the data into the users table")

	parser.add_option('--create_table',
					action="store_true", dest="create_table",
					help="This will build/rebuild a new table")

	parser.add_option('--dry_run',
					action="store", type="string",
					dest="dry_run", help="Runs the script without inserting into the users table")

	parser.add_option('-u',
					action="store", dest="username",
					help="MySQL username -- required")

	parser.add_option('-p',
					action="store", dest="password",
					help="MySQL password -- required")

	parser.add_option('--host',
					action="store", dest="host",
					help="MySQL host -- required")

	(options, args) = parser.parse_args()

	try:
		db = MySQLdb.connect(host=options.host, user=options.username, passwd=options.password, db="record")

		if options.file:
			parse_csvfile(options.file, db)

		elif options.create_table:
			create_table(db)

		elif options.dry_run:
			include_table_insertion = False
			print "This option will run the script without saving the data into the table"
			parse_csvfile(options.dry_run, db, include_table_insertion)

	except TypeError as e:
		print "Please provide username, password and host to connect to the database"

	else:
		db.close()

main()
