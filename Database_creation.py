"""
===============================================================================
 Script Name   : create_harvard_tables.py
 Description   : 
    This script initializes a local SQLite database named 'harvard_db.sqlite3' 
    and creates the core tables used for storing artifact information related 
    to the Harvard Art Museum dataset.

    Tables Created:
      1. artifact_metadata  → Stores general information about each artifact 
         (title, culture, century, medium, etc.)
      2. artifact_media      → Stores media-related attributes (image count, 
         media count, rank, and date range), linked to artifact_metadata via 
         a foreign key.
      3. artifact_colors     → Stores color data (spectrum, hue, percentage, 
         CSS3 value) for each artifact, also linked via a foreign key.

    After creating the tables, the script confirms their creation, commits 
    changes, lists all existing tables, and closes the database connection.

 Author         : Prasath RK
 Last Modified  : 10-10-2025
 Contact        : https://www.linkedin.com/in/prasath-rk-552076258/
===============================================================================
"""


import sqlite3
#dbconnection
conn=sqlite3.connect("harvard_db.sqlite3")
cursor=conn.cursor()
#Table1    creating Table artifact_metadata
cursor.execute("""
CREATE TABLE IF NOT EXISTS artifact_metadata (
    id INTEGER PRIMARY KEY,
    title TEXT,
    culture TEXT,
    period TEXT,
    century TEXT,
    medium TEXT,
    dimensions TEXT,
    description TEXT,
    department TEXT,
    classification TEXT,
    accessionyear INTEGER,
    accessionmethod TEXT
)
""")

# Table 2: artifact media (with foreign key to artifact_metadata)
cursor.execute("""
CREATE TABLE IF NOT EXISTS artifact_media (
    objectid INTEGER PRIMARY KEY,
    imagecount INTEGER,
    mediacount INTEGER,
    colorcount INTEGER,
    rank INTEGER,
    datebegin INTEGER,
    dateend INTEGER,
    FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
)
""")
print("✅ Table 'artifact_metadata' created successfully!")
#Table 3: artifact_colors(with Foreign key that links this color record to its corresponding artifact. )
cursor.execute("""
CREATE TABLE IF NOT EXISTS artifact_colors (
    objectid INTEGER PRIMARY KEY,
    color TEXT,
    spectrum TEXT,
    hue TEXT,
    percent REAL,
    css3 TEXT,
    FOREIGN KEY (objectid) REFERENCES artifact_metadata(id)
)
""")

print("✅ Table 'artifact_colors' created successfully!")

# Commit changes
conn.commit()

print("✅ Table 'artifact_colors' created successfully!")

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for i in tables:
  print(i)
# Close connection
conn.close()