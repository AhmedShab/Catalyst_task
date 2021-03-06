# Script Task
### This Python script reads CSV file and inserts it into MySQL database. You will need to have your own MYSQL installed on your local machine.

##### The CSV file structure is the following:

| name  | surname | email |
| :------:|:-------:| :-----:|
| Ahmed | Shaaban | ahmed@gmail.com |

##### It must contain name, surname, and email. There should not be any spaces between the three columns in order for the script to run. Your name and/or surname could be empty but you have to provide an email. Your email should be unique. Otherwise, your data (name, surname, and email) won't be saved.

##### Before running the script, you would need to install the `MySQLdb` package if you don't have it already.

##### To run this script, type `python user_upload.py -u [username] -p [password] --host [hostname]` followed by one of these commands:

     --file [csv file name] - This is the name of the CSV to be parsed
     --create_table - This will build/rebuild a new table
     --dry_run [csv file name] - This runs the script without inserting into the users table

##### Can also use `python user_upload.py -h/--help` to display the above commands.

##### I used `record` as my database name, this script will require that.

##### I wrote on this script assuming I have to have one script called `user_upload.py`

##### I have written a few tests for this script. You can find it in `test_user_upload.py`. All you need to do to run it is to have `mock` package and then run this command: `python test_user_upload.py `. 
