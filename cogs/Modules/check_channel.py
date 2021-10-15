from discord.ext import commands
import discord
import sqlite3


def check_channel(client, channel_id):
    database = sqlite3.connect("Data/database.db")
    cur = database.cursor()
    cur.execute(f"SELECT * FROM cmdlist WHERE channelId = {channel_id}")
    liste = cur.fetchall()
    return len(liste) > 0