# Constants and configuration
import os
import sys

# Application info
APP_NAME = "Rock V2 - Discord Server Cloner"
APP_VERSION = "2.0"
VERSION = '2'
SUPPORT_LINK = "https://discord.gg/twNGK45BuH"

# Paths
RESOURCES = os.path.join(os.path.dirname(__file__), '..', 'resources')
ICON_PATH = "icon.ico"

# Default settings
DEFAULT_PREFERENCES = {
    'guild_edit': True,
    'channels_delete': True,
    'roles_delete': True,
    'roles_create': True,
    'categories_create': True,
    'channels_create': True,
    'emojis_create': False
}