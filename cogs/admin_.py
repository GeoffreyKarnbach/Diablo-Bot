import discord
from discord.ext import commands
import time
import sqlite3
import string
import random
import json
from datetime import datetime
from discord.utils import get
import asyncio

from .Modules.maxPoints import *
from .Modules.permissions import *
from .Modules.logs import *
from .Modules.paginator import *
from .Modules.check_channel import *


class AdminCommands(commands.Cog):

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
    async def acmdlist(self, ctx):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute("SELECT * FROM cmdlist")
        all_channels = self.cur.fetchall()
        await ctx.send("List of all cmd channels:")
        string = ""
        for loop in all_channels:
            channel = discord.utils.get(self.client.get_all_channels(), id=loop[0])
            string = string + "Channel ID: " + str(loop[0]) + " -|- Channel Name: "+str(channel.name)+"\n"
        await ctx.send("```" + string + "```")
        await log(self.client, f"Acmdlist by {ctx.message.author.mention}", 2)

    @commands.command()
    async def acmdadd(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            if channel is not None:
                self.cur.execute(f"INSERT INTO cmdlist VALUES({channel.id})")
                self.db.commit()
                await ctx.send("Channel ID has sucessfully been added to the list of cmd channels.")

                log_str = f"[A] {ctx.message.author.mention} allowed commands of the vouch system to be used in {channel.mention}"
                await log(self.client, log_str, 2)
            else:
                await ctx.send("You didn't send a valid channel ID.")
        except:
            await ctx.send("You didn't send a valid channel ID.")

    @commands.command()
    async def acmddel(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            self.cur.execute(f"DELETE FROM cmdlist WHERE channelId = {channel.id}")
            self.db.commit()
            await ctx.send("Sucessfully removed the channel ID from the list.")

            log_str = f"[A] {ctx.message.author.mention} prohibited commands of the vouch system to be used in {channel.mention}"
            await log(self.client, log_str, 2)
        except:
            await ctx.send("The given ID is not allready in the list.")

    @commands.command()
    async def asetminchar(self, ctx, nb: int):

        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return

        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            with open("Configuration/server_setting.json", "r") as file:
                data = json.load(file)
            data["minimum"] = int(nb)
            with open("Configuration/server_setting.json", 'w') as outfile:
                json.dump(data, outfile)
            await ctx.send(f"Minimum limit of reason sucessfully changed to {int(nb)}.")

            log_str = f"[A] {ctx.message.author.mention} has set the **minimum characters** a vouch reason needs to:  {nb}"
            await log(self.client, log_str, 2)

        except:
            await ctx.send("You need to enter a valid integer.")

    @commands.command()
    async def asetmaxchar(self, ctx, nb: int):

        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            with open("Configuration/server_setting.json", "r") as file:
                data = json.load(file)
            data["maximum"] = int(nb)
            with open("Configuration/server_setting.json", 'w') as outfile:
                json.dump(data, outfile)
            await ctx.send(f"Maximum limit of reason sucessfully changed to {int(nb)}.")

            log_str = f"[A] {ctx.message.author.mention} has set the **maximum characters** a vouch reason needs to:  {nb}"
            await log(self.client, log_str, 2)

        except:
            await ctx.send("You need to enter a valid integer.")

    @commands.command()
    async def asetulogs(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            if channel is not None:
                self.cur.execute(f"INSERT INTO loglist VALUES({channel.id},{0})")
                self.db.commit()
                await ctx.send("Channel ID has sucessfully been added to the list of the user logs.")

                log_str = f"[A] {ctx.message.author.mention} has set channel {channel.mention} as a **USERS logs channel**"
                await log(self.client, log_str, 2)
            else:
                await ctx.send("You didn't send a valid channel ID.")
        except:
            await ctx.send("You didn't send a valid channel ID.")

    @commands.command()
    async def asetmlogs(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            if channel is not None:
                self.cur.execute(f"INSERT INTO loglist VALUES({channel.id},{1})")
                self.db.commit()
                await ctx.send("Channel ID has sucessfully been added to the list of the user logs.")

                log_str = f"[A] {ctx.message.author.mention} has set channel {channel.mention} as a **MODS logs channel**"
                await log(self.client, log_str, 2)
            else:
                await ctx.send("You didn't send a valid channel ID.")
        except:
            await ctx.send("You didn't send a valid channel ID.")

    @commands.command()
    async def asetalogs(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            if channel is not None:
                self.cur.execute(f"INSERT INTO loglist VALUES({channel.id},{2})")
                self.db.commit()
                await ctx.send("Channel ID has sucessfully been added to the list of the user logs.")

                log_str = f"[A] {ctx.message.author.mention} has set channel {channel.mention} as a **ADMIN logs channel**"
                await log(self.client, log_str, 2)
            else:
                await ctx.send("You didn't send a valid channel ID.")
        except:
            await ctx.send("You didn't send a valid channel ID.")

    @commands.command()
    async def asetologs(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            if channel is not None:
                self.cur.execute(f"INSERT INTO loglist VALUES({channel.id},{3})")
                self.db.commit()
                await ctx.send("Channel ID has sucessfully been added to the list of the user logs.")

                log_str = f"[A] {ctx.message.author.mention} has set channel {channel.mention} as a **OWNER logs channel**"
                await log(self.client, log_str, 2)
            else:
                await ctx.send("You didn't send a valid channel ID.")
        except:
            await ctx.send("You didn't send a valid channel ID.")

    @commands.command()
    async def alogsdel(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        try:
            self.cur.execute(f"DELETE FROM loglist WHERE channelId = {channel.id}")
            self.db.commit()
            await ctx.send("Sucessfully removed the channel ID from the logs channel list.")

            log_str = f"[A] {ctx.message.author.mention} **revoked** {channel.mention} from being a **logs channel**"
            await log(self.client, log_str, 2)
        except:
            await ctx.send("The given ID is not allready in the list.")

    @commands.command()
    async def alogslist(self, ctx):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute("SELECT * FROM loglist")
        all_channels = self.cur.fetchall()
        await ctx.send("List of all cmd channels:")
        string = ""
        for loop in all_channels:
            channel = discord.utils.get(self.client.get_all_channels(), id=loop[0])
            string = string + "Channel ID: " + str(loop[0]) + "  -|-  Type: " + str(loop[1]) +"  -|-  Channel name: "+ str(channel.name).ljust(15)+"\n"
        await ctx.send("```" + string + "```")
        await log(self.client, f"Alogslist by {ctx.message.author.mention}", 2)

    @commands.command()
    async def araid(self, ctx):

        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        with open('Configuration/server_setting.json') as json_file:
            data = json.load(json_file)
            current_raid = data["raid"]

        if current_raid == 0:
            data["raid"] = 1
            with open("Configuration/server_setting.json", 'w') as outfile:
                json.dump(data, outfile)
            await ctx.send(f"Enabled raid mode.")

            log_str = f"[A] {ctx.message.author.mention} **deactivated** the vouch system."
            await log(self.client, log_str, 2)

        else:
            data["raid"] = 0
            with open("Configuration/server_setting.json", 'w') as outfile:
                json.dump(data, outfile)
            await ctx.send(f"Disabled raid mode.")

            log_str = f"[A] {ctx.message.author.mention} **activated** the vouch system."
            await log(self.client, log_str, 2)

    @commands.command()
    async def aprep(self, ctx, associated_user: discord.User, *, reason):

        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        if not self.check_msg_length(reason):
            await ctx.send(f"The length of the message has to be between {8} and {25}.")
            return

        try:

            if associated_user.id == ctx.message.author.id:
                await ctx.send("Can't change reputation of yourself.")
                return

            id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=7))

            self.cur.execute(f"INSERT INTO reputations VALUES(?,?,?,?,?,?)",
                             [id, 2, reason, int(time.time()), associated_user.id, ctx.message.author.id])
            self.db.commit()

            self.cur.execute(
                f"INSERT INTO today VALUES({ctx.message.author.id},{associated_user.id},{int(time.time())})")
            self.db.commit()

            await ctx.send(
                f"Reputation modification sucessfull. {ctx.message.author.mention} gave one point to {associated_user.mention} for the reason: {reason}.")
            await rep_log(self.client, f"APREP from {ctx.message.author.id} to {associated_user.id}")

            log_str = f"[A] [:blue_circle: | {id}] From {ctx.message.author.mention} to {associated_user.mention}, reason : {reason}."
            await log(self.client, log_str, 2)

        except Exception as e:
            await ctx.send("An error occured. Please try again later.")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")

    @commands.command()
    async def adhelpchannel(self, ctx, channel: discord.TextChannel):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        with open("Configuration/server_setting.json", "r") as file:
            data = json.load(file)
        data["help_channel"] = int(channel.id)
        with open("Configuration/server_setting.json", 'w') as outfile:
            json.dump(data, outfile)

        await ctx.send(f"Sucessfully set the channel ({channel.name}, {channel.id}) to help channel.")

    @commands.command()
    async def amodlist(self, ctx):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute("SELECT * FROM roleLevel")
        all_roles = self.cur.fetchall()
        await ctx.send("List of all roles and authorization level:")
        string = ""
        for loop in all_roles:
            roles = ctx.message.guild.get_role(loop[0])
            string = string + "Role ID: " + str(loop[0]) + "   |   Auth Level: " + str(loop[1]) + "   |   Role name: "+str(roles.name)+ "\n"

        await ctx.send("```" + string + "```")
        await log(self.client, f"Amodlist by {ctx.message.author.mention}", 2)

    @commands.command()
    async def aroleadd(self, ctx, role: discord.Role, valeur: int):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute(f"SELECT * FROM pointRole WHERE roleId = {role.id}")
        result = self.cur.fetchall()

        if len(result) != 0:
            self.cur.execute(f"DELETE FROM pointRole WHERE roleID = {role.id}")

        self.cur.execute(f"INSERT INTO pointRole VALUES({role.id},{valeur})")
        self.db.commit()

        await ctx.send(
            f"Sucessfully added points on role ({str(role.id)}, {str(role.mention)}) with amount {str(valeur)}")

        result.append([0,0])
        log_str = f"[A] {ctx.message.author.mention} has set the number of points {role.mention} can give each day to {valeur}\n\nOld: {result[0][1]} \n New: {valeur}"
        await log(self.client, log_str, 2)

    @commands.command()
    async def arolelock(self, ctx, role: discord.Role, *, reason: str):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute(f"SELECT * FROM lockedRoles WHERE roleID = {role.id}")
        inside = self.cur.fetchall()

        if permission_value(1,ctx) <= auth_by_role_id(role.id, ctx):
            await ctx.send("Missing permissions to lock that role.")
            return

        if len(inside) == 0:
            

            self.cur.execute(f"INSERT INTO lockedRoles VALUES({role.id})")
            self.db.commit()

            await ctx.send(f"Sucessfully locked role ({str(role.id)}, {str(role.mention)})")
            log_str = f"[A] {ctx.message.author.mention} **locked** {role.mention}.\n\nReason: {reason}"
            await log(self.client, log_str, 2)
        else:
            self.cur.execute(f"DELETE FROM lockedRoles WHERE roleID = {role.id}")
            self.db.commit()

            await ctx.send(f"Sucessfully unlocked role ({str(role.id)}, {str(role.mention)})")
            log_str = f"[A] {ctx.message.author.mention} **unlocked** {role.mention}.\n\nReason: {reason}"
            await log(self.client, log_str, 2)
        
    @commands.command()
    async def arolelocklist(self, ctx):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute("SELECT * FROM lockedRoles")
        all_roles = self.cur.fetchall()
        await ctx.send("List of all locked roles:")
        string = ""
        for loop in all_roles:
            role = get(ctx.message.guild.roles, id=loop[0])
            string = string + "Role: " + str(role.mention)

        await ctx.send(string)
        await log(self.client, f"Arolelocklist by {ctx.message.author.mention}", 2)

    @commands.command()
    async def aroledel(self, ctx, role: discord.Role):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute(f"DELETE FROM pointRole WHERE roleId = {role.id}")
        self.db.commit()

        await ctx.send(f"Sucessfully removed giveable points on role ({str(role.id)}, {str(role.mention)})")
        await log(self.client, f"Aroledel by {ctx.message.author.mention}", 2)

    @commands.command()
    async def arolelist(self, ctx):
        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        self.cur.execute("SELECT * FROM pointRole")
        all_roles = self.cur.fetchall()
        await ctx.send("List of all roles and giveable points:")
        string = ""
        for loop in all_roles:
            roles = ctx.message.guild.get_role(loop[0])
            string = string + "Role ID: " + str(loop[0]) + "   |   Point Ammount: " + str(loop[1])  + "   |   Role name: "+str(roles.name)+ "\n"

        await ctx.send("```" + string + "```")
        await log(self.client, f"Arolelist by {ctx.message.author.mention}", 2)

    @commands.command()
    async def amrep(self, ctx, associated_user: discord.User, *, reason):

        if not hasPermissions(7, ctx):
            await ctx.send("Missing permissions to execute that command.")
            return
        
        if not can_send_message_role(ctx):
            await ctx.send("[Locked !] Vouch system utilization has been temporarily suspended for one of your roles roles.")
            return

        if not self.check_msg_length(reason):
            await ctx.send(f"The length of the message has to be between {8} and {25}.")
            return

        try:

            if associated_user.id == ctx.message.author.id:
                await ctx.send("Can't change reputation of yourself.")
                return

            id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=7))

            self.cur.execute(f"INSERT INTO reputations VALUES(?,?,?,?,?,?)",
                             [id, 0, reason, int(time.time()), associated_user.id, ctx.message.author.id])
            self.db.commit()

            self.cur.execute(
                f"INSERT INTO today VALUES({ctx.message.author.id},{associated_user.id},{int(time.time())})")
            self.db.commit()

            await ctx.send(
                f"Reputation modification sucessfull. {ctx.message.author.mention} took one point from {associated_user.mention} for the reason: {reason}.")
            await rep_log(self.client, f"AMREP from {ctx.message.author.id} to {associated_user.id}")

            log_str = f"[A] [:red_circle: | {id}] From {ctx.message.author.mention} to {associated_user.mention}, reason : {reason}."
            await log(self.client, log_str, 2)

        except Exception as e:
            await ctx.send("An error occured. Please try again later.")

            with open('Configuration/server_setting.json') as json_file:
                data = json.load(json_file)
                channel_id = data["error-channel-id"]

            channel = self.client.get_channel(channel_id)
            await channel.send("Error message:```" + str(e) + "```")


def setup(client):
    client.add_cog(AdminCommands(client))
