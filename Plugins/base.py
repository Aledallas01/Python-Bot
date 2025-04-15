import discord
from discord.ext import commands
import random

#############################################
# Configurazione del Bot e degli Intent
#############################################
# Imposta gli Intents (necessario per accedere al contenuto dei messaggi)
intents = discord.Intents.default()
intents.message_content = True

# Crea l'istanza del bot con il prefisso "!"
bot = commands.Bot(command_prefix='!', intents=intents)
NAME = "INSERISCI_IL_NOME_DEL_TUO_BOT_QUI"



#############################################
# Helper: Creazione di Embed Standardizzati
#############################################
def create_embed(title: str, description: str, color: int = 0x00ff00, thumbnail: str = None):
    embed = discord.Embed(title=title, description=description, color=color)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    embed.set_footer(text=f"Plugin Base - Powered by {NAME}")
    return embed



#############################################
# Helper: Genera una Password Casual
#############################################
def generate_password(length: int) -> str:
    elements = '+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    # Utilizza una list comprehension per generare la password in modo conciso
    return ''.join(random.choice(elements) for _ in range(length))



#############################################
# Comandi Base
#############################################

@commands.command()
async def ciao(ctx):
    # Creazione di un embed personalizzato per il saluto
    embed = create_embed("Ciao!", f"Salve, sono **{bot.user}**!", color=0x00ff00)
    await ctx.send(embed=embed)
    

@commands.command()
async def arrivederci(ctx):
    embed = create_embed("Arrivederci!", "A presto, torna presto a trovarci!", color=0xff5555)
    await ctx.send(embed=embed)
    

@commands.command()
async def password(ctx, larghezza: int):
    try:
        # Genera la password utilizzando la funzione helper
        pwd = generate_password(larghezza)
        # Crea un embed personalizzato per mostrare il risultato
        embed = create_embed("Password Generata",
                             f"Ecco la tua password segreta:\n**{pwd}**",
                             color=0x00ff00)
        # Aggiungi una sezione esplicativa
        embed.add_field(name="Nota", value="Ricorda di conservare questa password in un luogo sicuro.", inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Si è verificato un errore nella generazione della password: {e}")



#############################################
# Setup del plugin Base
#############################################
def setup(bot):
    # Registra i comandi nel bot
    bot.add_command(ciao)
    bot.add_command(arrivederci)
    bot.add_command(password)
