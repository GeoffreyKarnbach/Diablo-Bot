import discord
from discord.ext import commands
import sqlite3
import asyncio

from .Modules.check_channel import*
from .Modules.permissions import*
from .Modules.paginator import*
from .Modules.command_list import*

class Help(commands.Cog):

    def __init__(self,client):
        self.client = client
        self.db = sqlite3.connect("Data/database.db")

    @commands.command(aliases=['help'])
    async def rephelp(self, ctx, nb = None):

        if not can_send_message_raid(ctx):
            await ctx.send("[Information] Vouch system has been temporarily deactivated by administrators.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return
        
        

        if not check_channel(self.client, ctx.message.channel.id):
            msg = await ctx.send("Can't use commands in this channel. Message will be deleted in 5 seconds.")
            await asyncio.sleep(5)
            await msg.delete()
            await ctx.message.delete()
            return

        all_roles = ctx.message.author.roles
        auth_level = permission_value(ctx.message.author.id, ctx)
        
        embed_list = []

        if nb is None:
            for loop in range(auth_level+1):
                embedVar = discord.Embed(title=f"({loop}) Level commands:", color=0x00ff00)
                for lopp in commands_per_level[loop]:
                    embedVar.add_field(name=lopp[0], value=lopp[1], inline = False)

                embed_list.append(embedVar)
        else:
            auth_level = permission_value(ctx.message.author.id, ctx)
            if auth_level < int(nb):
                embedVar = discord.Embed(title=f"Missing authorization to see that help category.", color=0x00ff00)
                embed_list.append(embedVar)
            else:
                embedVar = discord.Embed(title=f"({int(nb)}) Level commands:", color=0x00ff00)
                for lopp in commands_per_level[int(nb)]:
                    embedVar.add_field(name=lopp[0], value=lopp[1], inline=False)

                embed_list.append(embedVar)

        with open("Configuration/server_setting.json", "r") as file:
            data = json.load(file)
        help_channel = self.client.get_channel(int(data["help_channel"]))

        embedVar = discord.Embed(title="Global informations.", color=0x00ff00)
        embedVar.add_field(name="Help channel:", value=help_channel.mention, inline = False)
        embedVar.add_field(name="Developer:", value="<@450259740153479189>", inline = False)
        embed_list.append(embedVar)
            
        if len(embed_list) <= 1:
            await ctx.send(embed=embed_list[0]) 
        else:
            await add_paginator(self.client, ctx, embed_list, self.db)


def setup(client):
    client.add_cog(Help(client))