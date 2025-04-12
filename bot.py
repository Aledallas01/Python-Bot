import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore, Style, init
import os
import importlib.util
import time
import asyncio
import random

# Inizializza colorama (per garantire il reset dei colori su ogni riga)
init(autoreset=True)

# Configurazione degli intents
intents = discord.Intents.default()
intents.message_content = True

# Creazione del bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Variabili di configurazione
TOKEN = "MTM1NDg0MTc3MDczMDcyMTQ3Mw.GKu0Pt.wndFvzLkdkPa_nlLPvLBh4NBxUaZU-01KzYA_I"
PREFIX = "!"

GUILD_ID = 1354841382916718744       # ID del Server
OWNER_ROLE_ID = 1354852422916243700    # ID del ruolo OWNER
STAFF_ROLE_ID = 1355235876942250120    # ID del ruolo STAFF
MUTED_ROLE_ID = 1354911951649767514    # ID del ruolo Muted

TICKET_CATEGORY_ID = 1355241599357030610      # ID della categoria dei ticket aperti
TICKET_CLOSE_CATEGORY_ID = 1359914726909280321  # ID della categoria dei ticket chiusi

# Dizionario dei comandi con descrizione
COMANDI = {
    "ciao": "Comando per salutare",
    "arrivederci": "Comando per salutare",
    "password": "Comando per generare una password casuale",
    "comandi": "Comando per visualizzare la lista dei comandi",
    "add": "Comando per sommare due numeri",
    "sub": "Comando per sottrarre due numeri",
    "mul": "Comando per moltiplicare due numeri",
    "div": "Comando per dividere due numeri",
    "server": "Comando per mostrare informazioni sul server",
    "role": "Comando per aggiungere o rimuovere un ruolo",
    "joined": "Comando per mostrare quando un membro è entrato nel server",
    "role_add": "Comando per aggiungere o rimuovere un ruolo a un membro",
    "online": "Comando per mostrare i membri online",
    "offline": "Comando per mostrare i membri offline",
    "ban": "Comando per bannare un membro",
    "unban": "Comando per unban un membro",
    "kick": "Comando per espellere un membro",
    "mute": "Comando per mutare un membro",
    "unmute": "Comando per unmutare un membro",
    "testa_o_croce": "Gioco del testa o croce",
    "leggi": "Comando per leggere il contenuto di un file",
    "scrivi": "Comando per scrivere del testo in un file",
    "aggiungi": "Comando per aggiungere testo a un file",
    "clear": "Comando per pulire un certo numero di messaggi",
    "ticket": "Comando per aprire un ticket",
}

# Logo del bot (raw string per evitare problemi con i caratteri di escape)
logo = r"""\n
 ____           __    __                             ____    ____    _____            
/\  _`\        /\ \__/\ \                           /\  _`\ /\  _`\ /\  __`\          
\ \ \L\ \__  __\ \ ,_\ \ \___     ___     ___       \ \ \L\ \ \ \L\ \ \ \/\ \         
 \ \ ,__/\ \/\ \\ \ \/\ \  _ `\  / __`\ /' _ `\      \ \ ,__/\ \ ,  /\ \ \ \ \        
  \ \ \/\ \ \_\ \\ \ \_\ \ \ \ \/\ \L\ \/\ \/\ \      \ \ \/  \ \ \\ \\ \ \_\ \       
   \ \_\ \/`____ \\ \__\\ \_\ \_\ \____/\ \_\ \_\      \ \_\   \ \_\ \_\ \_____\      
    \/_/  `/___/> \\/__/ \/_/\/_/\/___/  \/_/\/_/       \/_/    \/_/\/ /\/_____/      
             /\___/                                                                   
             \/__/                                                                    
"""

# Funzione per stampare la schermata iniziale nel terminale
def start_screen():
    print(Fore.YELLOW + logo)
    version = "1.0.0"  # Versione del bot
    header_text = f"v{version} - Bot di Discord"
    space_amount = (84 - len(header_text)) // 2
    print(Fore.CYAN + " " * space_amount + header_text)
    print(Fore.CYAN + "=" * 84)
    print(Fore.GREEN + "Bot avviato. Attendere...")
    time.sleep(1)  # Pausa di 1 secondo per miglior effetto visivo

# Funzione per caricare manualmente i plugin dalla cartella "Plugins"
def load_all_plugins(bot, folder="Plugins"):
    # Calcola il percorso assoluto della cartella "Plugins" rispetto al file corrente
    folder_path = os.path.join(os.path.dirname(__file__), folder)
    print(Fore.CYAN + "Caricamento dei plugin dalla cartella:", folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            # Salta i plugin non ancora completi (economy ed xp)
            if filename[:-3].lower() in ["economy", "xp"]:
                print(Fore.YELLOW + f"{filename[:-3].capitalize()} non caricato (non completo).")
                continue
            plugin_name = filename[:-3]
            filepath = os.path.join(folder_path, filename)
            try:
                spec = importlib.util.spec_from_file_location(plugin_name, filepath)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "setup"):
                    module.setup(bot)
                    print(Fore.GREEN + f"{plugin_name.capitalize()} caricato.")
                else:
                    print(Fore.RED + f"{plugin_name.capitalize()} non contiene la funzione setup().")
            except Exception as e:
                print(Fore.RED + f"Errore nel caricamento di {plugin_name}: {e}")

# Importa importlib.util necessario per il caricamento manuale dei plugin
import importlib.util

# Evento per il log dei comandi eseguiti
@bot.event
async def on_command(ctx):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_str = f"{Fore.GREEN}{ctx.author}{Style.RESET_ALL}"

    # Mappatura dei comandi relativi ai ticket e delle azioni specifiche
    ticket_action_map = {
         "ticket": "APERTO",
    }
    
    command_name = ctx.command.name.lower()
    
    # Se il comando riguarda i ticket, usa un formato speciale:
    if command_name in ticket_action_map:
        action = ticket_action_map[command_name]
        ticket_name = ctx.channel.name if ctx.channel.name.lower().startswith("ticket-") else "Non specificato"
        log_message = ()

    else:
        descrizione = COMANDI.get(command_name, "Descrizione non disponibile")
        log_message = (
            f"{Fore.BLUE}{current_time}{Style.RESET_ALL} | "
            f"{user_str}: {Fore.YELLOW}{ctx.command}{Style.RESET_ALL} - {Fore.MAGENTA}{descrizione}{Style.RESET_ALL}"
        )
    print(log_message)

# Evento on_ready: carica i plugin e mostra informazioni di login
@bot.event
async def on_ready():
    load_all_plugins(bot)  # Chiamata sincrona, perché load_all_plugins è definita in modo sincrono
    print(Fore.GREEN + f'Logged in as {bot.user} (ID: {bot.user.id})')

# Mostra la schermata iniziale
start_screen()

# Avvio del bot
bot.run(TOKEN)
