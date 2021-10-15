import discord
from discord.ext import commands
import sqlite3
import json

from .Modules.permissions import *
from .Modules.logs import *


class OwnerCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("Data/database.db")
        self.cur = self.db.cursor()

    @commands.command()
    async def oprefix(self, ctx, *, prefix="."):
        if not hasPermissions(8, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return

        with open('Configuration/server_setting.json', "r") as json_file:
            data = json.load(json_file)
            data["prefix"] = prefix

        with open('Configuration/server_setting.json', "w") as json_file:
            json_file.write(json.dumps(data))

        await ctx.send(f"New prefix will be {prefix}")

        log_str = f"[Core] The Vouch system command prefix is now: **{prefix}**"
        await log(self.client, log_str, 3)

    @commands.command()
    async def orolelvl(self, ctx, role: discord.Role, valeur: int):
        if not hasPermissions(8, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return

        self.cur.execute(f"SELECT * FROM roleLevel WHERE roleId = {role.id}")
        result = self.cur.fetchall()

        if len(result) != 0:
            self.cur.execute(f"DELETE FROM roleLevel WHERE roleId = {role.id}")
            await ctx.send(
                f"Successfully updated authorization level on role ({str(role.id)}, {str(role.mention)}) with level {str(valeur)}")

        self.cur.execute(f"INSERT INTO roleLevel VALUES({role.id},{valeur})")
        self.db.commit()

        if len(result) == 0:
            await ctx.send(
                f"Successfully added authorization level on role ({str(role.id)}, {str(role.mention)}) with level {str(valeur)}")
            
        log_str = f"[Core] {role.mention} has been granted a **level {valeur}** access to Vouch System commmands."
        await log(self.client, log_str, 3)

    @commands.command()
    async def odelrolelvl(self, ctx, role: discord.Role):
        if not hasPermissions(8, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return

        self.cur.execute(f"DELETE FROM roleLevel WHERE roleId = {role.id}")
        self.db.commit()

        await ctx.send(f"Sucessfully removed authorization level on role ({str(role.id)}, {str(role.mention)})")
    
        log_str = f"[Core] {role.mention} has lost his authorization level on Vouch System commmands."
        await log(self.client, log_str, 3)

    @commands.command()
    async def oroleban(self, ctx, role: discord.Role):
        if not hasPermissions(8, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return

        self.cur.execute(f"INSERT INTO roleLevel VALUES({role.id},{0})")
        self.db.commit()

        await ctx.send(f"Sucessfully added role ({str(role.id)}, {str(role.mention)}) to banned role list (LVL 0).")
        log_str = f"[Core] Users with the role {role.mention} now have a level 0 access to Vouch system commands."
        await log(self.client, log_str, 3)

    @commands.command()
    async def odelroleban(self, ctx, role: discord.Role):
        if not hasPermissions(8, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return

        self.cur.execute(f"DELETE FROM roleLevel WHERE roleId = {role.id}")
        self.db.commit()

        await ctx.send(f"Sucessfully removed role ({str(role.id)}, {str(role.mention)}) from banned role list (LVL 0).")
        log_str = f"[Core] Role {role.mention} is not restricted to level 0 commands anymore. Use **OROLELEVEL** command to set up its new permissions."
        await log(self.client, log_str, 3)


def setup(client):
    client.add_cog(OwnerCommands(client))
