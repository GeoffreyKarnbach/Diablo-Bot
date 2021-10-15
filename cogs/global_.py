import discord
from discord.ext import commands
import sqlite3
from .Modules.paginator import*
from .Modules.permissions import*
from .Modules.command_list import*
from difflib import SequenceMatcher

class Global(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("Data/database.db")
    
    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Hello new member, "+member.name)

    @commands.command()
    async def ping(self,ctx):
        await ctx.send("Pong!")

    @commands.command(aliases=['s'])
    async def shutdown(self,ctx):
        if ctx.message.author.id == 450259740153479189:
            await ctx.send("Bot shuting down.")
            exit(-1)
        else:
            await ctx.send("Missing permissions.")
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        await paginator_edit(event, self.client)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        maxi = 0
        maxi_element = None
        auth_level = permission_value(ctx.message.author.id, ctx)
        for loop in commands_per_level[:auth_level]:
            for lopp in loop:
                if self.similar(lopp[0], ctx.message.content) > maxi:
                    maxi = self.similar(lopp[0], ctx.message.content)
                    maxi_element = lopp
                    
        if maxi != 0:
            await ctx.send("No such command or missing argument. Did you mean:")
            await ctx.send(f"```Command: {maxi_element[0]} \n\nUsage: {maxi_element[1]}```")
        else:
            await ctx.send("No similar command found. Lookup the command list with **.rephelp**.")

      
def setup(client):
    client.add_cog(Global(client))




    
    

