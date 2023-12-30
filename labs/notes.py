# import subprocess

# script = '''
# tell application "Notes"
#     set noteList to name of every note
#     return noteList
# end tell
# '''

# process = subprocess.Popen(['osascript', '-'],
#                            stdin=subprocess.PIPE,
#                            stdout=subprocess.PIPE,
#                            stderr=subprocess.PIPE,
#                            universal_newlines=True)
# stdout, stderr = process.communicate(script)

# print(stdout)  # This will print the list of note titles


import sqlite3
import os

# Path to the Notes database
db_path = os.path.expanduser('~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite')

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SQL query to select all notes (this is a simplified example)
query = "SELECT * FROM ZICCLOUDSYNCINGOBJECT;"  # You might need to adjust this query

# Execute the query
cursor.execute(query)

# Fetch and print all notes
for row in cursor.fetchall():
    print(row)

# Close the connection
cursor.close()
conn.close()
