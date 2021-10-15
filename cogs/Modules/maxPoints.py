import sqlite3

def get_max_points(user, ctx):
    points = 5

    db = sqlite3.connect("Data/database.db")
    cur = db.cursor()

    cur.execute("SELECT * FROM pointRole")
    roleList = cur.fetchall()

    user_roles_obj = user.roles
    user_roles = []

    for loop in user_roles_obj:
        user_roles.append(loop.id)
        
    for loop in roleList:
        if loop[0] in user_roles:
            points += loop[1]
            
    return points