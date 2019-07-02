import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

#Create Fresh tables

cur.executescript('''

DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    artist_id INTEGER,
    title TEXT UNIQUE
);

CREATE TABLE Track (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER, 
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# Read filename from User, default is "Library.xml" from itunes
fname = input('Enter file name: ')
if ( len(fname) < 1) : fname = 'Library.xml'

# Function to parse a single XML line and return the value of required tag
def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

# Parse the XML to get the <dict> block of depth 3
stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Item count: ', len(all))

# Extract the required values using the lookup function
for entry in all:
    if (lookup(entry, 'Track ID') is None): continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None: continue #Sanity check
    
    print(name, artist, album, count, rating, length) #Optional, real stuff happens in the DB

    # Populate the DB tables
    cur.execute('''INSERT OR IGNORE INTO Artist (name) VALUES ( ? )''', (artist, ) )
    cur.execute('''SELECT id FROM Artist where name = ? ''', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) VALUES ( ?, ? )''', (album, artist_id, ) )
    cur.execute('''SELECT id FROM Album where title = ? ''', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, len, rating, count)
        VALUES (?, ?, ?, ?, ?)''',
        (name, album_id, length, rating, count))

    #Done
    conn.commit()