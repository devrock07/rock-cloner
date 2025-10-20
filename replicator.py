import discord
import asyncio
import random
import aiohttp
from colorama import Fore, init, Style

init()

def print_bar():
    print(Fore.MAGENTA + "+------------------------------------------------------+" + Style.RESET_ALL)

def print_add(msg):
    print_bar()
    print(Fore.GREEN + f"[+] {msg}" + Style.RESET_ALL)

def print_delete(msg):
    print_bar()
    print(Fore.RED + f"[-] {msg}" + Style.RESET_ALL)

def print_warning(msg):
    print_bar()
    print(Fore.YELLOW + f"[!] {msg}" + Style.RESET_ALL)

def print_error(msg):
    print_bar()
    print(Fore.MAGENTA + f"[x] {msg}" + Style.RESET_ALL)

def print_info(msg):
    print_bar()
    print(Fore.CYAN + f"{msg}" + Style.RESET_ALL)

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        if not guild_to.me or not guild_to.me.guild_permissions.manage_roles:
            print_warning("Skipping role deletion: Missing 'Manage Roles' permission.")
            return
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Deleted role: {role.name}")
                    await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"No permission to delete role: {role.name}")
            except discord.HTTPException as e:
                print_error(f"Error deleting role {role.name}: {e}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me or not guild_to.me.guild_permissions.manage_roles:
            print_warning("Skipping role creation: Missing 'Manage Roles' permission.")
            return
        roles = [r for r in guild_from.roles if r.name != "@everyone"][::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Created role: {role.name}")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"No permission to create role: {role.name}")
            except discord.HTTPException as e:
                print_error(f"Error creating role {role.name}: {e}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        if not guild_to.me or not guild_to.me.guild_permissions.manage_channels:
            print_warning("Skipping channel deletion: Missing 'Manage Channels' permission.")
            return
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted channel: {channel.name}")
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                print_error(f"No permission to delete channel: {channel.name}")
            except discord.HTTPException as e:
                print_error(f"Error deleting channel {channel.name}: {e}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me or not guild_to.me.guild_permissions.manage_channels:
            print_warning("Skipping category creation: Missing 'Manage Channels' permission.")
            return
        for category in guild_from.categories:
            try:
                overwrites_to = {}
                for key, value in category.overwrites.items():
                    if isinstance(key, discord.Role):
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        if role:
                            overwrites_to[role] = value
                await guild_to.create_category(name=category.name, overwrites=overwrites_to)
                print_add(f"Created category: {category.name}")
                await asyncio.sleep(0.2)
            except discord.Forbidden:
                print_error(f"No permission to create category: {category.name}")
            except discord.HTTPException as e:
                print_error(f"Error creating category {category.name}: {e}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me or not guild_to.me.guild_permissions.manage_channels:
            print_warning("Skipping channel creation: Missing 'Manage Channels' permission.")
            return

        for channel in guild_from.text_channels:
            try:
                category = discord.utils.get(guild_to.categories, name=channel.category.name) if channel.category else None
                await guild_to.create_text_channel(
                    name=channel.name,
                    topic=channel.topic or "",
                    slowmode_delay=channel.slowmode_delay,
                    nsfw=channel.nsfw,
                    position=channel.position,
                    category=category
                )
                print_add(f"Created text channel: {channel.name}")
                await asyncio.sleep(0.2)
            except Exception as e:
                print_error(f"Error creating text channel {channel.name}: {e}")

        for channel in guild_from.voice_channels:
            try:
                category = discord.utils.get(guild_to.categories, name=channel.category.name) if channel.category else None
                await guild_to.create_voice_channel(
                    name=channel.name,
                    user_limit=channel.user_limit,
                    bitrate=channel.bitrate,
                    position=channel.position,
                    category=category
                )
                print_add(f"Created voice channel: {channel.name}")
                await asyncio.sleep(0.2)
            except Exception as e:
                print_error(f"Error creating voice channel {channel.name}: {e}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me or not guild_to.me.guild_permissions.manage_emojis:
            print_warning("Skipping emoji creation: Missing 'Manage Emojis' permission.")
            return
        for emoji in guild_from.emojis:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(emoji.url)) as resp:
                        if resp.status == 200:
                            image_data = await resp.read()
                            await guild_to.create_custom_emoji(name=emoji.name, image=image_data)
                            print_add(f"Created emoji: {emoji.name}")
                            await asyncio.sleep(0.4)
            except Exception as e:
                print_error(f"Error creating emoji {emoji.name}: {e}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        if not guild_to.me or not guild_to.me.guild_permissions.manage_guild:
            print_warning("Skipping guild edit: Missing 'Manage Guild' permission.")
            return
        try:
            icon_content = None
            if guild_from.icon:
                async with aiohttp.ClientSession() as session:
                    async with session.get(guild_from.icon.url) as resp:
                        if resp.status == 200:
                            icon_content = await resp.read()
            await guild_to.edit(name=guild_from.name, icon=icon_content)
            print_add("Edited server name and icon")
        except Exception as e:
            print_error(f"Error editing guild: {e}")

    @staticmethod
    def log_server_structure(guild_from: discord.Guild):
        print_add(f"Logging structure of: {guild_from.name}")
        print_info("Roles:")
        for role in guild_from.roles:
            if role.name != "@everyone":
                print(f" - {role.name} (Color: {role.colour})")
        print_info("Categories and Channels:")
        for category in guild_from.categories:
            print(f" > Category: {category.name}")
            for ch in category.channels:
                print(f"    - {ch.name} ({'Text' if isinstance(ch, discord.TextChannel) else 'Voice'})")
        print_info("Emojis:")
        for emoji in guild_from.emojis:
            print(f" - {emoji.name} ({emoji.url})")
