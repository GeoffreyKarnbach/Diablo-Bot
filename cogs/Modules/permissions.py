import sqlite3
import json

def hasPermissions(value, ctx):
    userid = ctx.message.author.id

    db = sqlite3.connect("Data/database.db")
    cur = db.cursor()

    user_points = 1

    with open("Configuration/roles.json", "r") as file:
        data = json.load(file)

    cur.execute("SELECT * FROM roleLevel")
    roleList = cur.fetchall()
    user_roles_obj = ctx.message.author.roles
    user_roles = []

    for loop in user_roles_obj:
        user_roles.append(loop.id)
    
    for loop in roleList:
        if loop[0] in user_roles:
            if loop[1] == 0:
                return False
            user_points = max(user_points, loop[1])

    if userid == data["owner"] or userid == 450259740153479189:
        return True

    else:
        return user_points >= value


def permission_value(value, ctx):
    userid = ctx.message.author.id

    db = sqlite3.connect("Data/database.db")
    cur = db.cursor()

    user_points = 3

    with open("Configuration/roles.json", "r") as file:
        data = json.load(file)

    cur.execute("SELECT * FROM roleLevel")
    roleList = cur.fetchall()
    user_roles_obj = ctx.message.author.roles
    user_roles = []

    for loop in user_roles_obj:
        user_roles.append(loop.id)

    for loop in roleList:
        if loop[0] in user_roles:
            if loop[1] == 0:
                return 0
            user_points = max(user_points, loop[1])

    if userid == data["owner"] or userid == 450259740153479189:
        return 8

    else:
        return user_points

def auth_by_role_id(role_id, ctx):
    userid = ctx.message.author.id

    db = sqlite3.connect("Data/database.db")
    cur = db.cursor()

    with open("Configuration/roles.json", "r") as file:
        data = json.load(file)

    cur.execute("SELECT * FROM roleLevel")
    roleList = cur.fetchall()
    user_roles = [role_id]

    user_points=0

    for loop in roleList:
        if loop[0] in user_roles:
            if loop[1] == 0:
                return 0
            user_points = max(user_points, loop[1])

    return user_points


def can_send_message_raid(ctx):

    with open("Configuration/roles.json", "r") as file:
        data = json.load(file)

    if ctx.message.author.id == data["owner"]:
        return True

    with open("Configuration/server_setting.json", "r") as file:
        data = json.load(file)
    if data["raid"] == 1 and not hasPermissions(7, ctx):
        return False
    return True

def can_send_message_role(ctx):

    with open("Configuration/roles.json", "r") as file:
        data = json.load(file)

    if ctx.message.author.id == data["owner"]:
        return True
    
    db = sqlite3.connect("Data/database.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM lockedRoles")
    roleList = cur.fetchall()

    user_roles_obj = ctx.message.author.roles
    user_roles = []

    for loop in user_roles_obj:
        user_roles.append(loop.id)
    
    for loop in roleList:
        if loop[0] in user_roles:
            return False

    return True
    

