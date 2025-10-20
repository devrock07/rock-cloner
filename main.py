import os
import sys
import time
import platform
import traceback
import asyncio
import psutil
from pathlib import Path
from threading import Thread
from typing import Dict, Optional, Any
import subprocess

# --- Fix audioop missing in Python 3.13+ ---
import types
from types import ModuleType
from typing import cast

if sys.version_info >= (3, 13):
    fake_audioop = cast(ModuleType, types.ModuleType("audioop"))
    setattr(fake_audioop, "ratecv", lambda *args, **kwargs: (b"", (0, 0)))
    sys.modules["audioop"] = fake_audioop

# --- Other imports ---
import discord
import inquirer
import aiohttp
from colorama import Fore, init as colorama_init, Style
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    SpinnerColumn,
    TimeElapsedColumn,
    BarColumn,
    TextColumn
)
from rich.live import Live
from rich.text import Text
from rich.spinner import Spinner
from pyfiglet import Figlet
from replicator import Clone

# === Init ===
colorama_init()
console = Console()
version = '2'
versao_python = sys.version.split()[0]
client = discord.Client()
SUPPORT_LINK = "https://www.quantheon.xyz/"
RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')

# === Utility Functions ===
def restart():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# pygame audio player
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
try:
    import pygame
    class AudioPlayer:
        def __init__(self, console):
            self.console = console
            try:
                pygame.mixer.init()
                self.initialized = True
            except Exception as e:
                self.console.print(f"[yellow]• Pygame audio failed to initialize: {str(e)}[/]")
                self.initialized = False
            
        def play_audio(self, file: str, loop: bool = False):
            if not self.initialized:
                return
            full_path = os.path.join(RESOURCES, file)
            if os.path.exists(full_path):
                try:
                    sound = pygame.mixer.Sound(full_path)
                    sound.play(loops=-1 if loop else 0)
                except Exception as e:
                    self.console.print(f"[red]• Audio error: {str(e)}[/]")
                    
        def stop(self):
            if self.initialized:
                pygame.mixer.stop()
                
    audio_player = AudioPlayer(console)
except ImportError:
    console.print("[yellow]• Pygame not installed. Audio disabled.[/]")
    class DummyAudioPlayer:
        def play_audio(self, *args, **kwargs): pass
        def stop(self): pass
    audio_player = DummyAudioPlayer()

# === UI Functions ===
def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def ascii_banner(text: str, font: str = 'slant') -> str:
    return Figlet(font=font).renderText(text)

def print_logo():
    banner = ascii_banner("ROCK V2")
    console.print(Panel.fit(
        f"[magenta]{banner}[/]",
        title="[blue]Discord Server Cloner[/]",
        subtitle="[cyan]By DEVROCK[/]",
        border_style="purple",
        padding=(1, 2)
    ))

def print_status(text: str, color: str = "cyan"):
    console.print(f"[{color}]• {text}[/]")

def big_loading_spinner(task_message: str, duration: float = 3.0):
    spinner = Spinner(name="dots12", style="blue", text=Text(f"⢋⠠ {task_message}...", style="blue"))
    start_time = time.time()
    
    with Live(spinner, refresh_per_second=20) as live:
        while time.time() - start_time < duration:
            time.sleep(0.05)
            spinner.text = Text(f"⢋⠠ {task_message}... {time.time() - start_time:.1f}s", style="blue")
        spinner.text = Text(f"⢋⠠ {task_message} - Done!", style="green")
        time.sleep(0.5)

def show_progress_bar(task_message: str):
    with Progress(
        SpinnerColumn(style="blue", speed=1.0),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="blue", finished_style="green"),
        TimeElapsedColumn(),
        transient=True,
        expand=True
    ) as progress:
        task = progress.add_task(f"[blue]{task_message}[/]", total=100)
        for i in range(100):
            progress.update(task, advance=1)
            time.sleep(0.03)

# === Menu Panels ===
def show_documentation():
    doc_text = f"""[purple]
[blue]Welcome to Rock V2 - Discord Server Cloner[/]

Clone:
• Roles
• Categories
• Channels
• Emojis (optional)
• Server icon and name

Instructions:
1. Provide a valid user token
2. Enter Source & Destination Server IDs
3. Configure what to clone

[cyan]Need help? Join our support server:[/]
[blue]{SUPPORT_LINK}[/][/purple]"""
    console.print(Panel.fit(doc_text, 
                         title="📘 Documentation", 
                         border_style="blue",
                         padding=(1, 2),
                         subtitle="[yellow]Press ENTER to continue[/]"))
    input(f"\n{Fore.CYAN}Press ENTER to return to menu...{Style.RESET_ALL}")

def show_tips():
    tips = """[cyan]
Shortcuts:
- [Y] confirm inputs
- [N] retry input
- [Ctrl+C] exit

Make sure:
- You're in both servers
- Bot has required permissions
- Server IDs are valid
[/cyan]"""
    console.print(Panel.fit(tips, 
                          title="💡 Tips & Shortcuts", 
                          border_style="magenta",
                          padding=(1, 2),
                          subtitle="[yellow]Press ENTER to continue[/]"))
    input(f"\n{Fore.CYAN}Press ENTER to return to menu...{Style.RESET_ALL}")

def get_user_preferences() -> Dict[str, bool]:
    preferences = {
        'guild_edit': True,
        'channels_delete': True,
        'roles_delete': True,
        'roles_create': True,
        'categories_create': True,
        'channels_create': True,
        'emojis_create': False
    }
    panel_content = "\n".join([f"[magenta]•[/] {k.replace('_', ' ').capitalize()}: [cyan]{v}[/]" for k, v in preferences.items()])
    console.print(Panel.fit(panel_content, 
                         title="Preferences Summary", 
                         style="blue",
                         padding=(1, 2)))

    answers = inquirer.prompt([inquirer.List('reconfigure', message='Reconfigure settings?', choices=['Yes', 'No'], default='No')])
    if answers and answers['reconfigure'] == 'Yes':
        questions = [
            inquirer.Confirm('guild_edit', message='Edit server icon/name?', default=True),
            inquirer.Confirm('channels_delete', message='Delete channels?', default=True),
            inquirer.Confirm('roles_delete', message='Delete roles?', default=True),
            inquirer.Confirm('roles_create', message='Clone roles?', default=True),
            inquirer.Confirm('categories_create', message='Clone categories?', default=True),
            inquirer.Confirm('channels_create', message='Clone channels?', default=True),
            inquirer.Confirm('emojis_create', message='Clone emojis?', default=False)
        ]
        new_prefs = inquirer.prompt(questions)
        if new_prefs:
            preferences.update(new_prefs)
    clear_screen()
    print_logo()
    return preferences

def show_main_menu():
    audio_player.play_audio("loading.mp3", loop=True)
    big_loading_spinner("Booting Rock V2", 3.5)
    audio_player.stop()
    
    while True:
        clear_screen()
        print_logo()
        menu_options = Panel.fit(
            "[blue]1. Run Rock V2[/]\n"
            "[purple]2. Show Documentation[/]\n"
            "[cyan]3. Show Tips & Shortcuts[/]\n"
            "[red]4. Exit[/]",
            title="Main Menu",
            border_style="green",
            padding=(1, 2)
        )
        console.print(menu_options)

        choice = input(f"\n{Fore.CYAN}Choose an option (1/2/3/4): {Style.RESET_ALL}")
        if choice == '1':
            return
        elif choice == '2':
            clear_screen()
            print_logo()
            show_documentation()
        elif choice == '3':
            clear_screen()
            print_logo()
            show_tips()
        elif choice == '4':
            print_status("Exiting... Goodbye!", "red")
            sys.exit()
        else:
            print_status("Invalid choice, try again!", "red")
            time.sleep(2)

# === Main Cloning Process ===
async def perform_cloning(guild_to: discord.Guild, guild_from: discord.Guild, preferences: Dict[str, bool]):
    try:
        audio_player.play_audio("cloning.mp3", loop=True)
        
        tasks = []
        if preferences['channels_delete']:
            show_progress_bar("Deleting existing channels")
            tasks.append(Clone.channels_delete(guild_to))
        if preferences['roles_delete']:
            show_progress_bar("Deleting existing roles")
            tasks.append(Clone.roles_delete(guild_to))
        if preferences['roles_create']:
            show_progress_bar("Cloning roles")
            tasks.append(Clone.roles_create(guild_to, guild_from))
        if preferences['categories_create']:
            show_progress_bar("Cloning categories")
            tasks.append(Clone.categories_create(guild_to, guild_from))
        if preferences['channels_create']:
            show_progress_bar("Cloning channels")
            tasks.append(Clone.channels_create(guild_to, guild_from))
        if preferences['emojis_create']:
            show_progress_bar("Cloning emojis")
            tasks.append(Clone.emojis_create(guild_to, guild_from))
        if preferences['guild_edit']:
            show_progress_bar("Updating server settings")
            tasks.append(Clone.guild_edit(guild_to, guild_from))

        for task in tasks:
            try:
                await task
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = getattr(e, 'retry_after', 5)
                    print_status(f"Rate limited for {retry_after}s", "yellow")
                    await asyncio.sleep(retry_after)
                    await task
                else:
                    raise
        
        audio_player.stop()
        audio_player.play_audio("done.mp3")
        
    except Exception as e:
        audio_player.stop()
        raise

# === Main Execution ===
show_main_menu()
clear_screen()
print_logo()

while True:
    token = input(f"{Fore.YELLOW} [1] Your Token\n   {Fore.BLUE}> {Style.RESET_ALL}")
    guild_s = input(f"{Fore.YELLOW} [2] Source Server ID\n   {Fore.BLUE}> {Style.RESET_ALL}")
    guild = input(f"{Fore.YELLOW} [3] Destination Server ID\n   {Fore.BLUE}> {Style.RESET_ALL}")

    clear_screen()
    print_logo()

    info_panel = Panel.fit(
        f"[cyan]Token: {'*' * len(token)}\n"
        f"Source Server ID: {guild_s}\n"
        f"Destination Server ID: {guild}[/]",
        title="Input Summary",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(info_panel)

    confirm = input(f"\n{Fore.YELLOW} Is the above information correct? (Y/N)\n   {Fore.BLUE}> {Style.RESET_ALL}").strip().upper()
    if confirm == 'Y':
        if not (guild_s.isnumeric() and guild.isnumeric()):
            print_status("Server IDs must be numbers!", "red")
            input("Press Enter to retry...")
            continue
        break

input_guild_id, output_guild_id = guild_s, guild

@client.event
async def on_ready():
    try:
        clear_screen()
        print_logo()
        
        table = Table(title="Rock V2 Environment", style="blue", expand=True)
        table.add_column("Component", style="cyan", justify="center")
        table.add_column("Version", style="magenta", justify="center")
        table.add_row("Rock V2", version)
        table.add_row("discord.py-self", discord.__version__)
        table.add_row("Python", versao_python)
        console.print(table)

        big_loading_spinner("Authenticating", 2)
        
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))
        if not guild_from or not guild_to:
            raise ValueError("Invalid guilds! Check server IDs and access.")

        preferences = get_user_preferences()
        if not any(preferences.values()):
            preferences = {k: True for k in preferences}

        if guild_to and guild_to.me and guild_to.me.guild_permissions:
            permissions = guild_to.me.guild_permissions
            if not (permissions.manage_guild and permissions.manage_roles and permissions.manage_channels):
                print_status("Permissions insufficient, switching to log-only.", "red")
                Clone.log_server_structure(guild_from)
            else:
                await perform_cloning(guild_to, guild_from, preferences)

        console.print(Panel.fit(
            "[magenta]Your server was cloned successfully.[/]", 
            title="✅ Completed", 
            border_style="cyan",
            padding=(1, 2),
            subtitle="[yellow]Rock Cloner...[/]"
        ))
        await asyncio.sleep(10)
        await client.close()

    except Exception as e:
        audio_player.stop()
        print_status(f"Error: {str(e)}", "red")
        traceback.print_exc()
        console.print(Panel.fit(
            f"[red]Check token and server access.[/]\n[cyan]Need help?[/] [blue]{SUPPORT_LINK}[/]",
            title="❌ Error", 
            border_style="red",
            padding=(1, 2)
        ))
        big_loading_spinner("Restarting", 10)
        restart()

try:
    client.run(token)
except discord.LoginFailure:
    audio_player.stop()
    print_status("Invalid token!", "red")
    big_loading_spinner("Restarting", 5)
    restart()
