from discord.ext import commands
import discord
import json
import sqlite3

async def add_paginator(client, ctx, content, db):
    message = await ctx.send(embed = content[0])
    await message.add_reaction("🏠")
    await message.add_reaction("⏪")
    await message.add_reaction("◀")
    await message.add_reaction("▶")
    await message.add_reaction("⏩")
    await message.add_reaction("↪")

    page_counter = 0
    liste = []
    for loop in content:
        liste.append(loop.to_dict())
    
    db.cursor().execute(f"INSERT INTO paginator VALUES(?,?,?,?)",[0, len(content),message.id, json.dumps(liste)])
    db.commit()
    
    '''
    :house: -> 0
    :rewind: -> -10
    :arrow_backward: -> -1
    :arrow_forward: -> +1
    :fast_forward: -> +10
    :arrow_right_hook: -> len(content)-1
    '''

async def paginator_edit(event, client):
    if event.user_id != 775112625406869514:
        db = sqlite3.connect("Data/database.db")
        cusor = db.cursor()
        cusor.execute(f"SELECT * FROM paginator WHERE messageId = {event.message_id}")
        info = cusor.fetchall()
        if info != []:
            info = info[0]
            if str(event.emoji) == "🏠":
                to_load = 0
            elif str(event.emoji) == "⏪":
                to_load = max(info[0]-10, 0)
            elif str(event.emoji) == "◀":
                to_load = max(info[0]-1,0)
            elif str(event.emoji) == "▶":
                to_load = min(info[0]+1, info[1]-1)
            elif str(event.emoji) == "⏩":
                to_load = min(info[0]+10, info[1]-1)
            elif str(event.emoji) == "↪":
                to_load = info[1]-1

            cusor.execute(f"UPDATE paginator SET page = {to_load} WHERE messageId = {event.message_id}")
            db.commit()

            content = json.loads(info[3])

            new_embed = discord.Embed.from_dict(content[to_load])

            channel = client.get_channel(event.channel_id)
            msg = await channel.fetch_message(event.message_id)
            await msg.edit(embed = new_embed)
            
            await msg.clear_reactions()
            await msg.add_reaction("🏠")
            await msg.add_reaction("⏪")
            await msg.add_reaction("◀")
            await msg.add_reaction("▶")
            await msg.add_reaction("⏩")
            await msg.add_reaction("↪")


    
    