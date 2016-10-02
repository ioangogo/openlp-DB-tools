import os,platform
import sqlite3
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

datalocation={"Windows":str(os.getenv('APPDATA')) + "\\openlp\\" , "Linux": str(os.getenv('HOME')) + "/.local/share/openlp/"}

cos = platform.system()
print("Current os is " + cos) 

dbpath = datalocation[cos] + "songs/songs.sqlite"

print("What data base do you want to work on \r\n1. OpenLP's \r\n2. select file using select dialog")
uin = input("Select one of the options, defult 1:")

if str(uin) == "2":
  dbpath = filedialog.askopenfilename(filetypes=(("SQLite Database", "*.sqlite"),
                                                 ("All files", "*.*")))

print("Connecting to database at " + dbpath)
conn = sqlite3.connect(dbpath)
tb_exists = "SELECT name FROM sqlite_master WHERE type='table' AND name='songs_songbooks'"

if not conn.execute(tb_exists).fetchone():
 print("OpenLP 2.2 detected")
 print("Checking For phantom books")
 result = conn.execute("update songs set song_book_id = NULL where not exists (select 1 from song_books where songs.song_book_id = song_books.id)")
 result.fetchone()
else:
 print("OpenLP 2.4 detected")
 print("Checking and removing links to phantom books")
 result = conn.execute("delete from songs_songbooks where not exists (select 1 from song_books where songs_songbooks.songbook_id = song_books.id)")
 result.fetchone()
conn.commit()
conn.close()
