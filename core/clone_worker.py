import asyncio
import discord
from PyQt6.QtCore import QThread, pyqtSignal

# Import the Clone class correctly
import sys
import os

# Add the core directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(current_dir, '..', 'core')
sys.path.insert(0, core_dir)

from clone_functions import Clone

class CloneWorker(QThread):
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, token, source_id, dest_id, preferences):
        super().__init__()
        self.token = token
        self.source_id = source_id
        self.dest_id = dest_id
        self.preferences = preferences
        self.client = None
        
    def run(self):
        try:
            asyncio.run(self._run_clone())
        except Exception as e:
            self.finished_signal.emit(False, str(e))
    
    async def _run_clone(self):
        try:
            # Create new client instance - using discord.py-self without Intents
            self.client = discord.Client()
            
            @self.client.event
            async def on_ready():
                try:
                    self.update_signal.emit("✅ Connected to Discord")
                    
                    guild_from = self.client.get_guild(int(self.source_id))
                    guild_to = self.client.get_guild(int(self.dest_id))
                    
                    if not guild_from:
                        raise ValueError(f"Could not access source server {self.source_id}")
                    if not guild_to:
                        raise ValueError(f"Could not access destination server {self.dest_id}")
                    
                    self.update_signal.emit(f"📁 Source: {guild_from.name}")
                    self.update_signal.emit(f"📁 Destination: {guild_to.name}")
                    
                    # Check permissions
                    if guild_to.me.guild_permissions:
                        permissions = guild_to.me.guild_permissions
                        if not (permissions.manage_guild and permissions.manage_roles and permissions.manage_channels):
                            self.update_signal.emit("⚠️  Insufficient permissions - some operations may fail")
                    
                    # Perform cloning
                    await self._perform_cloning(guild_to, guild_from)
                    self.finished_signal.emit(True, "Cloning completed successfully!")
                    
                except Exception as e:
                    self.finished_signal.emit(False, str(e))
                finally:
                    await self.client.close()
            
            self.update_signal.emit("🔑 Logging in to Discord...")
            await self.client.start(self.token)
            
        except Exception as e:
            self.finished_signal.emit(False, str(e))
    
    async def _perform_cloning(self, guild_to, guild_from):
        total_steps = sum(1 for v in self.preferences.values() if v)
        if total_steps == 0:
            return
            
        step_increment = 100 // total_steps
        current_progress = 0
        
        try:
            # Delete operations first
            if self.preferences.get('channels_delete', False):
                self.update_signal.emit("🗑️  Deleting existing channels...")
                await Clone.channels_delete(guild_to)
                current_progress += step_increment
                self.progress_signal.emit(current_progress)
                self.update_signal.emit("✅ Channels deleted")
                
            if self.preferences.get('roles_delete', False):
                self.update_signal.emit("🗑️  Deleting existing roles...")
                await Clone.roles_delete(guild_to)
                current_progress += step_increment
                self.progress_signal.emit(current_progress)
                self.update_signal.emit("✅ Roles deleted")
            
            # Create operations
            if self.preferences.get('roles_create', False):
                self.update_signal.emit("👥 Cloning roles...")
                await Clone.roles_create(guild_to, guild_from)
                current_progress += step_increment
                self.progress_signal.emit(current_progress)
                self.update_signal.emit("✅ Roles cloned")
                
            if self.preferences.get('categories_create', False):
                self.update_signal.emit("📁 Cloning categories...")
                await Clone.categories_create(guild_to, guild_from)
                current_progress += step_increment
                self.progress_signal.emit(current_progress)
                self.update_signal.emit("✅ Categories cloned")
                
            if self.preferences.get('channels_create', False):
                self.update_signal.emit("💬 Cloning channels...")
                await Clone.channels_create(guild_to, guild_from)
                current_progress += step_increment
                self.progress_signal.emit(current_progress)
                self.update_signal.emit("✅ Channels cloned")
                
            if self.preferences.get('emojis_create', False):
                self.update_signal.emit("😀 Cloning emojis...")
                await Clone.emojis_create(guild_to, guild_from)
                current_progress += step_increment
                self.progress_signal.emit(current_progress)
                self.update_signal.emit("✅ Emojis cloned")
                
            if self.preferences.get('guild_edit', False):
                self.update_signal.emit("🖼️  Updating server settings...")
                await Clone.guild_edit(guild_to, guild_from)
                current_progress += step_increment
                self.progress_signal.emit(current_progress)
                self.update_signal.emit("✅ Server settings updated")
                
        except Exception as e:
            raise Exception(f"Cloning failed: {str(e)}")
        
        self.progress_signal.emit(100)