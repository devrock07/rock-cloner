import discord
import asyncio
import random
import aiohttp

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone" and not role.managed:
                    await role.delete()
                    await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                raise Exception(f"No permission to delete role: {role.name}")
            except discord.HTTPException as e:
                raise Exception(f"Error deleting role {role.name}: {e}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
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
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                raise Exception(f"No permission to create role: {role.name}")
            except discord.HTTPException as e:
                raise Exception(f"Error creating role {role.name}: {e}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                await asyncio.sleep(random.uniform(0.1, 0.3))
            except discord.Forbidden:
                raise Exception(f"No permission to delete channel: {channel.name}")
            except discord.HTTPException as e:
                raise Exception(f"Error deleting channel {channel.name}: {e}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for category in guild_from.categories:
            try:
                overwrites_to = {}
                for key, value in category.overwrites.items():
                    if isinstance(key, discord.Role):
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        if role:
                            overwrites_to[role] = value
                await guild_to.create_category(name=category.name, overwrites=overwrites_to)
                await asyncio.sleep(0.2)
            except discord.Forbidden:
                raise Exception(f"No permission to create category: {category.name}")
            except discord.HTTPException as e:
                raise Exception(f"Error creating category {category.name}: {e}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        # Text channels
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
                await asyncio.sleep(0.2)
            except Exception as e:
                raise Exception(f"Error creating text channel {channel.name}: {e}")

        # Voice channels
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
                await asyncio.sleep(0.2)
            except Exception as e:
                raise Exception(f"Error creating voice channel {channel.name}: {e}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for emoji in guild_from.emojis:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(emoji.url)) as resp:
                        if resp.status == 200:
                            image_data = await resp.read()
                            await guild_to.create_custom_emoji(name=emoji.name, image=image_data)
                            await asyncio.sleep(0.4)
            except Exception as e:
                raise Exception(f"Error creating emoji {emoji.name}: {e}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            icon_content = None
            if guild_from.icon:
                async with aiohttp.ClientSession() as session:
                    async with session.get(guild_from.icon.url) as resp:
                        if resp.status == 200:
                            icon_content = await resp.read()
            await guild_to.edit(name=guild_from.name, icon=icon_content)
        except Exception as e:
            raise Exception(f"Error editing guild: {e}")

    @staticmethod
    def log_server_structure(guild_from: discord.Guild):
        print(f"Server: {guild_from.name}")
        print("Roles:")
        for role in guild_from.roles:
            if role.name != "@everyone":
                print(f" - {role.name} (Color: {role.colour})")
        print("Categories and Channels:")
        for category in guild_from.categories:
            print(f" > Category: {category.name}")
            for ch in category.channels:
                print(f"    - {ch.name} ({'Text' if isinstance(ch, discord.TextChannel) else 'Voice'})")
        print("Emojis:")
        for emoji in guild_from.emojis:
            print(f" - {emoji.name} ({emoji.url})")