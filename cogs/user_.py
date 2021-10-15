import discord
from discord.ext import commands
import time
import sqlite3
import string
import random
import json
from datetime import datetime
import asyncio

from .Modules.maxPoints import *
from .Modules.permissions import *
from .Modules.logs import *
from .Modules.paginator import *
from .Modules.check_channel import *


class UserCommands(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.db = sqlite3.connect("Data/database.db")
        self.cur = self.db.cursor()

    def check_locked(self, id):
        self.cur.execute(f"SELECT * FROM locked WHERE user = {id}")
        locked_list = len(self.cur.fetchall())
        return locked_list != 0

    def check_msg_length(self, msg):
        with open("Configuration/server_setting.json", "r") as file:
            data = json.load(file)
        return len(msg) >= data["minimum"] and len(msg) <= data["maximum"]

    @commands.command()
    async def repcheck(self, ctx, arguments: discord.User = None):
        if not hasPermissions(1, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
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

        if arguments is None:
            associated_user = ctx.message.author
        else:
            associated_user = arguments

        self.cur.execute(f"SELECT * FROM reputations WHERE goal = {associated_user.id}")
        all_reputations = self.cur.fetchall()
        all_reputations.reverse()
        last_10 = all_reputations[0:min(len(all_reputations), 10)]

        embed_list = []
        # First page of embed
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

        embedVar.add_field(name="Most recent reputations.", value=string, inline=True)
        embed_list.append(embedVar)
        string = ""

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

        await log(self.client, f"Repcheck by {ctx.message.author.mention}", 0)

    @commands.command()
    async def prep(self, ctx, associated_user: discord.User, *, reason):

        if not hasPermissions(1, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return

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

        if not self.check_msg_length(reason):
            await ctx.send(f"The length of the message has to be between {8} and {25}.")
            return

        try:

            if self.check_locked(ctx.message.author.id):
                await ctx.send(
                    "You are currently locked from giving/receiving reputation. If you believe it is an error, contact support.")
                return

            if self.check_locked(associated_user.id):
                await ctx.send("Target user is currently locked from giving/receiving reputation.")
                return

            if associated_user.id == ctx.message.author.id:
                await ctx.send("Can't change reputation of yourself.")
                return

            self.cur.execute(f"SELECT * FROM today WHERE user = {ctx.message.author.id}")
            given_points = len(self.cur.fetchall())

            self.cur.execute(
                f"SELECT * FROM today WHERE user = {ctx.message.author.id} AND goal = {associated_user.id}")
            to_user = len(self.cur.fetchall())
            if given_points < get_max_points(ctx.message.author, ctx) and to_user < 1:

                id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=7))

                self.cur.execute(f"INSERT INTO reputations VALUES(?,?,?,?,?,?)",
                                 [id, 1, reason, int(time.time()), associated_user.id, ctx.message.author.id])
                self.db.commit()

                self.cur.execute(
                    f"INSERT INTO today VALUES({ctx.message.author.id},{associated_user.id},{int(time.time())})")
                self.db.commit()

                await ctx.send(
                    f"Reputation modification sucessfull. {ctx.message.author.mention} gave one point to {associated_user.mention} for the reason: {reason}. Reputation ID: {id}")
                await rep_log(self.client, f"PREP from {ctx.message.author.id} to {associated_user.id}")

                log_str = f"[:green_circle: | {id}] From {ctx.message.author.mention} to {associated_user.mention}, reason : {reason}."
                await log(self.client, log_str, 0)
            else:
                await ctx.send(
                    "You already gave the maximum amount of points for today (global or for a specific user). Reset at 00:00")

        except Exception as e:
            await ctx.send("An error occured. Please try again later.")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")

    @commands.command()
    async def mrep(self, ctx, associated_user: discord.User, *, reason):

        if not hasPermissions(1, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
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

        if not self.check_msg_length(reason):
            await ctx.send(f"The length of the message has to be between {8} and {25}.")
            return

        try:

            if self.check_locked(ctx.message.author.id):
                await ctx.send(
                    "You are currently locked from giving/receiving reputation. If you believe it is an error, contact support.")
                return

            if self.check_locked(associated_user.id):
                await ctx.send("Target user is currently locked from giving/receiving reputation.")
                return

            if associated_user.id == ctx.message.author.id:
                await ctx.send("Can't change reputation of yourself.")
                return

            self.cur.execute(f"SELECT * FROM today WHERE user = {ctx.message.author.id}")
            given_points = len(self.cur.fetchall())

            self.cur.execute(
                f"SELECT * FROM today WHERE user = {ctx.message.author.id} AND goal = {associated_user.id}")
            to_user = len(self.cur.fetchall())
            if given_points < get_max_points(ctx.message.author, ctx) and to_user < 1:

                id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=7))

                self.cur.execute(f"INSERT INTO reputations VALUES(?,?,?,?,?,?)",
                                 [id, 0, reason, int(time.time()), associated_user.id, ctx.message.author.id])
                self.db.commit()

                self.cur.execute(
                    f"INSERT INTO today VALUES({ctx.message.author.id},{associated_user.id},{int(time.time())})")
                self.db.commit()

                await ctx.send(
                    f"Reputation modification sucessfull. {ctx.message.author.mention} took one point from {associated_user.mention} for the reason: {reason}. Reputation ID: {id}")
                await rep_log(self.client, f"MREP from {ctx.message.author.id} to {associated_user.id}")

                log_str = f"[:red_circle: | {id}] From {ctx.message.author.mention} to {associated_user.mention}, reason : {reason}."
                await log(self.client, log_str, 0)
            else:
                await ctx.send(
                    "You already gave the maximum amount of points for today (global or for a specific user). Reset at 00:00")

        except Exception as e:
            await ctx.send("An error occured. Please try again later.")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")

    @commands.command()
    async def repedit(self, ctx, *, argument):
        if not hasPermissions(1, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
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

        try:
            author = ctx.message.author.id
            self.cur.execute(f"SELECT * FROM reputations WHERE origin = {author}")
            results = self.cur.fetchall()
            rep_id = results[-1][0]
            old_reason = results[-1][2]

            self.cur.execute(f"UPDATE reputations SET message = \"{argument}\" WHERE id = \"{rep_id}\"")
            self.db.commit()
            await ctx.send("Last reputation message sucessfully edited.")

            log_str = f"{ctx.message.author.mention} edited his last reputation, Rep.ID: {rep_id}\nBefore: {old_reason}\n\nAfter: {argument}"
            await log(self.client, log_str, 0)

        except Exception as e:
            await ctx.send("An error occured. Please try again later.")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")


def setup(client):
    client.add_cog(UserCommands(client))
