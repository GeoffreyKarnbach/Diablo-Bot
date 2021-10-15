from discord.ext import commands
import discord
import json
import sqlite3


async def log(client, content, category):
    db = sqlite3.connect("Data/database.db")
    cur = db.cursor()

    cur.execute(f"SELECT * FROM loglist WHERE category = {category}")
    result = cur.fetchall()

    for loop in result:
        channel = client.get_channel(loop[0])
        await channel.send(content)


async def rep_log(client, content):
    with open('Configuration/server_setting.json') as json_file:
        data = json.load(json_file)
        channel_id = data["log-channel-id"]
    
    channel = client.get_channel(channel_id)
    await channel.send(content)