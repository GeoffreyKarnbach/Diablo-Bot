from discord.ext import commands, tasks
import discord
import os
import sqlite3
from cogs.Modules.sql_utils import*
from cogs.Modules.json import*
import asyncio
from datetime import datetime
import json

###################################################################### COG UNLOAD + LOAD    ################################################
def load_all():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            print(f"===== {file[:-3]} loaded =====")
            client.load_extension("cogs."+file[:-3])

def unload_all():
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            print(f"===== {file[:-3]} unloaded =====")
            client.unload_extension("cogs."+file[:-3])


###################################################################### DATABASE MANAGING    ################################################
database = sqlite3.connect("Data/database.db")
create_table(database, "reputations", "(id text, type integer, message text, timestamp integer, goal integer, origin integer)")
create_table(database, "today", "(user integer, goal integer, timestamp integer)")
create_table(database, "locked", "(user integer, timestamp integer)")
create_table(database, "paginator", "(page integer, pageNB integer, messageId integer, embeds blob)")
create_table(database, "cmdlist", "(channelId integer)")
create_table(database, "loglist", "(channelId integer, category integer)")
create_table(database, "roleLevel", "(roleId integer, level integer)")
create_table(database, "pointRole", "(roleId integer, point integer)")
create_table(database, "lockedRoles", "(roleId integer)")
reset_table(database, "paginator")

######################################################################     DISCORD BOT    ################################################

async def get_pre(bot, message):
    with open('Configuration/server_setting.json') as json_file:
        data = json.load(json_file)
        prefix = data["prefix"]
    return prefix

client = commands.Bot(command_prefix = get_pre, help_command = None)

@client.command()
async def reload_cogs(ctx):
    if ctx.message.author.id != 450259740153479189:
        return
    unload_all()
    load_all()
    await ctx.send("All cogs have been reloaded.")

# Check if today reputation needs to be reset
async def check_today_db():
    while True:
        cur = database.cursor()
        cur.execute("SELECT * FROM today")
        results = cur.fetchall()
        if len(results) != 0:
            if datetime.fromtimestamp(results[0][2]).date() < datetime.today().date():
                reset_table(database, "today")
        await asyncio.sleep(60)
    
# Load all cogs
load_all()

######################################################################   RUN BOT WITH TOKEN    ################################################
client.loop.create_task(check_today_db())
client.run(readJSONFile('Configuration', 'token.json')['token'])
