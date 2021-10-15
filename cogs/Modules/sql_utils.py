import sqlite3

def create_table(db, tablename, values):
    db.cursor().execute(f"CREATE TABLE IF NOT EXISTS {tablename} {values}")  
    db.commit()

def reset_table(db, tablename):
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {tablename}")
    db.commit()
