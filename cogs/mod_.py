import discord
from discord.ext import commands
import sqlite3
import json
import time
from datetime import datetime

from .Modules.permissions import *
from .Modules.maxPoints import *
from .Modules.paginator import *
from .Modules.logs import *


class ModCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("Data/database.db")
        self.cur = self.db.cursor()

    def check_locked(self, userid):
        self.cur.execute(f"SELECT * FROM locked WHERE user = {userid}")
        res = self.cur.fetchall()
        if not res:
            return False
        else:
            return True

    @commands.command()
    async def mlocku(self, ctx, user: discord.Member, reason: str):
        if not hasPermissions(3, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            if self.check_locked(user.id):
                self.cur.execute(f"DELETE FROM locked WHERE user={user.id}")
                self.db.commit()

                await ctx.send(f"Unlocked {user.name} from receiving or giving reputation.")

                log_str = f"[M] {ctx.message.author.mention} unlocked {user.mention} \nReason: {reason}"
                await log(self.client, log_str, 1)
            else:
                self.cur.execute(f"INSERT INTO locked VALUES({user.id},{int(time.time())})")
                self.db.commit()

                await ctx.send(f"Locked {user.name} from receiving or giving reputation.")

                log_str = f"[M] {ctx.message.author.mention} locked {user.mention}, start time: {int(time.time())}\nReason: {reason}"
                await log(self.client, log_str, 1)

        except Exception as e:
            await ctx.send("An error occured. Please try again later.")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")
            await channel.send(
                f"Could not lock or unlock {user.name} from receiving or giving reputation, something went wrong accessing or modifying the database. Try again later or contact support.")

    @commands.command()
    async def mlockulist(self, ctx):
        if not hasPermissions(2, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            self.cur.execute(f"SELECT * FROM locked")

            embedVar = discord.Embed(title="List of all locked users:", color=0x00ff00)
            embedVar.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/820657616588898304/822787147928174652/imperius_by_emahrii_ddadoh1-fullview.png")

            string = ""
            data = self.cur.fetchall()
            
            for i in range(len(data)):
                current_user = await self.client.fetch_user(data[i][0])
                embedVar.add_field(name="\u200b",
                                    value="Locked user: " + current_user.mention + "```" + f"ID: {data[i][0]} \nStarttime: {datetime.fromtimestamp(data[i][1])}" + "```",
                                    inline=False)

            await ctx.send(embed=embedVar)
            await log(self.client, f"Mlockulist by {ctx.message.author.mention}", 1)

        except Exception as e:
            await ctx.send("An error occured. Please try again later.")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")
            await channel.send(f"Could not access DB, try again later or contact support.")

    @commands.command()
    async def mdayreset(self, ctx, user: discord.Member, *, reason: str):
        if not hasPermissions(4, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            self.cur.execute(f"DELETE FROM today WHERE user={user.id}")
            self.db.commit()
            await ctx.send("Reset the reputations points for today from  " + user.mention)

            log_str = f"[M] {ctx.message.author.mention} has reset {user.mention} daily reputation use, reason: {reason}"
            await log(self.client, log_str, 1)

        except Exception as e:
            await ctx.send("An error occured, ensure that you entered an actual user ID (only numbers).")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")

    @commands.command()
    async def mnuke(self, ctx, user: discord.Member, *, reason: str):

        if not hasPermissions(6, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            self.cur.execute(f"DELETE FROM reputations WHERE goal={user.id}")
            self.db.commit()
            await ctx.send("All the reputations deleted for " + user.mention)

            log_str = f"[M] {ctx.message.author.mention} nuked {user.mention} reputation history, reason: {reason}"
            await log(self.client, log_str, 1)

        except Exception as e:
            await ctx.send("An error occured, ensure that you entered an actual user ID (only numbers).")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")

    @commands.command()
    async def mrepdel(self, ctx, repid: str, *,reason: str):

        if not hasPermissions(5, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            self.cur.execute(f"SELECT * FROM reputations WHERE id=\"{repid}\"")
            result = self.cur.fetchall()

            self.cur.execute(f"DELETE FROM reputations WHERE id=\"{repid}\"")
            self.db.commit()
            await ctx.send("Delete reputation with ID: " + repid)

            dictionnary = {0: "mrep", 1: "prep"}
            log_str = f"[M] {ctx.message.author.mention} deleted the reputation :\n\nReputation: <{dictionnary[result[0][1]]}> <{result[0][2]}>\nRep.ID: {repid}"
            await log(self.client, log_str, 1)

        except Exception as e:
            await ctx.send(
                "An error occured, ensure that you entered an actual user reputation ID (no such ID found in DB).")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")

    @commands.command()
    async def mrepedit(self, ctx, repid: str, reptype: str, *, texte: str):

        if not hasPermissions(3, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        if reptype != "mrep" and reptype != "prep":
            await ctx.send("Need to specify reputation type (mrep/prep).")
            return

        try:

            self.cur.execute(f"SELECT * FROM reputations WHERE id=\"{repid}\"")
            result = self.cur.fetchall()

            self.cur.execute(f"UPDATE reputations SET message = \"{texte}\" WHERE id=\"{repid}\"")

            dictionnary = {"mrep": 0, "prep": 1}
            self.cur.execute(f"UPDATE reputations SET type = \"{dictionnary[reptype]}\" WHERE id=\"{repid}\"")

            self.db.commit()
            await ctx.send("Successfully modified reputation with id " + repid)

            dictionnary = {0: "mrep", 1: "prep"}
            log_str = f"[M] {ctx.message.author.mention} edited the reputation: \n\nBefore: {dictionnary[result[0][1]]} {result[0][2]}\nAfter: {reptype} {texte}\nRep.ID: {repid}"
            await log(self.client, log_str, 1)

        except Exception as e:
            await ctx.send(
                "An error occured, ensure that you entered an actual user reputation ID (no such ID found in DB).")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")

    @commands.command()
    async def mrepcheck(self, ctx, user: discord.Member = None):
        if not hasPermissions(2, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        if not user:
            associated_user = ctx.message.author
        else:
            associated_user = user


        self.cur.execute(f"SELECT * FROM reputations WHERE goal = {associated_user.id}")
        all_reputations = self.cur.fetchall()
        all_reputations.reverse()
        last_10 = all_reputations[0:min(len(all_reputations), 10)]

        embed_list = []

        embedVar = discord.Embed(title=str(associated_user), description="Score & Information", color=0x00ff00)
        embedVar.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/820657616588898304/822787147928174652/imperius_by_emahrii_ddadoh1-fullview.png")

        string = "\u200b"

        emote = {0: ":red_circle: ", 1: ":green_circle: ", 2: ":blue_circle:"}

        good = 0
        bad = 0

        for loop in range(len(last_10)):
            current_user = await self.client.fetch_user(last_10[loop][5])
            string += f"{datetime.fromtimestamp(last_10[loop][3]).strftime('%d-%m-%Y')} de {current_user.mention}:   {emote[last_10[loop][1]]} **:** {last_10[loop][2]}\n**ID: **{last_10[loop][0]}\n\n"
            if last_10[loop][1] == 0:
                bad += 1
            else:
                good += 1

        embedVar.add_field(name="+REP", value=str(good), inline=True)
        embedVar.add_field(name="-REP", value=str(bad), inline=True)
        try:
            embedVar.add_field(name="Score", value=str(int(good / (good + bad) * 100)) + "%", inline=True)
        except:
            embedVar.add_field(name="Score", value="0%", inline=True)

        embedVar.add_field(name="Max daily points:", value=str(get_max_points(associated_user, ctx)), inline=True)

        self.cur.execute(f"SELECT * FROM today WHERE user = {associated_user.id}")
        given_points = len(self.cur.fetchall())
        embedVar.add_field(name="Used daily points:", value=str(given_points), inline=True)

        embedVar.add_field(name="Most recent reputations.", value=string, inline=False)
        embed_list.append(embedVar)
        string = "\u200b"

        if len(all_reputations) > 10:
            for loop in range(10, len(all_reputations)):
                if (loop - 10) % 10 == 0 and loop != 10:
                    embedVar = discord.Embed(title=str(associated_user), description="Score & Information",
                                             color=0x00ff00)
                    embedVar.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/820657616588898304/822787147928174652/imperius_by_emahrii_ddadoh1-fullview.png")

                    embedVar.add_field(name="Most recent reputations.", value=string, inline=True)
                    embed_list.append(embedVar)
                    string = "\u200b"
                else:
                    string += f"{datetime.fromtimestamp(all_reputations[loop][3]).strftime('%d-%m-%Y')} de {current_user.mention}:   {emote[all_reputations[loop][1]]} **:** {all_reputations[loop][2]}\n**ID: **{all_reputations[loop][0]}\n\n"

        if string != "\u200b":
            embedVar = discord.Embed(title=str(associated_user), description="Score & Information", color=0x00ff00)
            embedVar.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/820657616588898304/822787147928174652/imperius_by_emahrii_ddadoh1-fullview.png")

            embedVar.add_field(name="Most recent reputations.", value=string, inline=True)
            embed_list.append(embedVar)

        if len(embed_list) <= 1:
            await ctx.send(embed=embed_list[0])
        else:
            await add_paginator(self.client, ctx, embed_list, self.db)
        await log(self.client, f"Mrepcheck by {ctx.message.author.mention}", 1)


def setup(client):
    client.add_cog(ModCommands(client))
