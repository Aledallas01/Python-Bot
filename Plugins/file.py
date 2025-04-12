import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ---------------------------------------
# Comandi per la gestione dei file
# ---------------------------------------

@commands.command()
async def leggi(ctx):
    """Legge il contenuto di un file."""
    file_path = 'new_file.txt'
    
    # Se il file non esiste, lo crea vuoto
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Testo di Esempio")  # Crea il file

    with open(file_path, 'r', encoding='utf-8') as f:
        contenuto = f.read()

    if contenuto:
        await ctx.send(contenuto)
    else:
        await ctx.send("📄 Il file è vuoto.")


@commands.command()
async def scrivi(ctx, testo: str):
    """Scrive del testo in un file."""
    with open('new_file.txt', 'w', encoding='utf-8') as f:
        # Sostituisce gli underscore con gli spazi
        testo = testo.replace('_', ' ')
        f.write(testo + '\n')
    await ctx.send(f"Testo scritto: {testo}")


@commands.command()
async def aggiungi(ctx, testo: str):
    """Aggiunge testo a un file."""
    with open('new_file.txt', 'a', encoding='utf-8') as f:
        f.write(testo + '\n')
    await ctx.send(f"Testo aggiunto: {testo}")


# La funzione setup è necessaria per caricare correttamente il plugin
def setup(bot):
    bot.add_command(leggi)
    bot.add_command(scrivi)
    bot.add_command(aggiungi)
