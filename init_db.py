import sqlite3

#Connect to database. if it does not exist yet, Python creates it
conn = sqlite3.connect("contest.db")
cursor = conn.cursor()

#This table stores information about each baking contest user
cursor.execute("""
CREATE TABLE IF NOT EXISTS BakingContestPeople (
    UserId INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Age INTEGER NOT NULL,
    PhoneNumber TEXT NOT NULL,
    SecurityLevel INTEGER NOT NULL,
    LoginPassword TEXT NOT NULL   
)    
""")

#This table stores the baking items entered into the contest
cursor.execute("""
CREATE TABLE IF NOT EXISTS BakingContestEntry (
    EntryId INTEGER PRIMARY KEY AUTOINCREMENT,
    UserId INTEGER NOT NULL,
    NameOfBakingItem TEXT NOT NULL,
    NumExcellentVotes INTEGER NOT NULL,
    NumOkVotes INTEGER NOT NULL,
    NumBadVotes INTEGER NOT NULL,
    FOREIGN KEY (UserId) REFERENCES BakingContestPeople(UserId)
)
""")

#Save the tables to the database
conn.commit()
conn.close()

print("Database tables created successfully!")

