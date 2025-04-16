import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore, Style, init
import os
import importlib.util
import time
import asyncio
import random



#############################################
# Inizializzazione di colorama per output colorato
#############################################
init(autoreset=True)



#############################################
# Configurazione degli Intents e creazione del bot
#############################################
intents = discord.Intents.default()
intents.message_content = True  # Abilita l’accesso al contenuto dei messaggi
bot = commands.Bot(command_prefix='!', intents=intents)



#############################################
# Variabili di configurazione globali
#############################################
TOKEN = "IL_TUO_TOKEN_QUI"
PREFIX = "!"
GUILD_ID = 1354841382916718744       # ID del Server
OWNER_ROLE_ID = 1354852422916243700    # ID del ruolo OWNER
STAFF_ROLE_ID = 1355235876942250120    # ID del ruolo STAFF
MUTED_ROLE_ID = 1354911951649767514    # ID del ruolo Muted
TICKET_CATEGORY_ID = 1355241599357030610      # ID della categoria dei ticket aperti
TICKET_CLOSE_CATEGORY_ID = 1359914726909280321  # ID della categoria dei ticket chiusi

# Dizionario dei comandi con descrizioni per il log
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



#############################################
# Logo e Schermata Iniziale del Bot
#############################################
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

def start_screen():
    """Stampa la schermata iniziale nel terminale."""
    print(Fore.YELLOW + logo)
    version = "1.0.0"  # Versione del Bot
    header_text = f"v{version} - Bot di Discord"
    space_amount = (84 - len(header_text)) // 2
    print(Fore.CYAN + " " * space_amount + header_text)
    print(Fore.CYAN + "=" * 84)
    print(Fore.GREEN + "Bot avviato. Attendere...")
    time.sleep(1)  # Pausa per effetto visivo



#############################################
# Caricamento dei Plugin
#############################################
def load_all_plugins(bot, folder="Plugins"):
    """Carica tutti i plugin dalla cartella specificata, saltando quelli non completi."""
    folder_path = os.path.join(os.path.dirname(__file__), folder)
    print(Fore.CYAN + "Caricamento dei plugin dalla cartella:", folder_path)
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            # Salta i plugin non completi (es. 'economy')
            if filename[:-3].lower() in ["economy"]:
                print(Fore.YELLOW + f"{filename[:-3].capitalize()} da completare.")
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



#############################################
# Evento: Log dei comandi eseguiti
#############################################
@bot.event
async def on_command(ctx):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_str = f"{Fore.GREEN}{ctx.author}{Style.RESET_ALL}"
    command_name = ctx.command.name.lower()

    # Controllo speciale per il comando ticket (puoi aggiungere altre eccezioni se necessario)
    if command_name == "ticket":
        # In caso di ticket, personalizza il log con eventuali informazioni sul canale
        ticket_name = ctx.channel.name if ctx.channel.name.lower().startswith("ticket-") else "Non specificato"
        log_message = f"{Fore.BLUE}{current_time}{Style.RESET_ALL} | {user_str}: {Fore.YELLOW}{ctx.command}{Style.RESET_ALL} - Ticket: {Fore.MAGENTA}{ticket_name}{Style.RESET_ALL}"
    else:
        descrizione = COMANDI.get(command_name, "Descrizione non disponibile")
        log_message = (
            f"{Fore.BLUE}{current_time}{Style.RESET_ALL} | "
            f"{user_str}: {Fore.YELLOW}{ctx.command}{Style.RESET_ALL} - {Fore.MAGENTA}{descrizione}{Style.RESET_ALL}"
        )
    print(log_message)



#############################################
# Evento: on_ready - Avvio del bot e caricamento dei plugin
#############################################
@bot.event
async def on_ready():
    load_all_plugins(bot)
    print(Fore.GREEN + f'Logged in as {bot.user} (ID: {bot.user.id})')



#############################################
# Main: Mostra la schermata iniziale e avvia il bot
#############################################
start_screen()
bot.run(TOKEN)
