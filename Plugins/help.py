import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

PREFIX = "!"
#dizionario dei comandi con descrizione
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

}

# ---------------------------------------
# Comandi di aiuto
# ---------------------------------------

@commands.command()
async def comandi(ctx):
    """Mostra la lista dei comandi disponibili."""
    help_message = "Ecco la lista dei comandi disponibili:\n"
    embed = discord.Embed(title="Comandi disponibili", description=help_message, color=0x00ff00)
    for comando, descrizione in COMANDI.items():
        embed.add_field(name=f"{PREFIX}{comando}", value=descrizione, inline=False)
    embed.set_footer(text="Usa !comandi per visualizzare questa lista.")


    await ctx.send(embed=embed)


# La funzione setup è necessaria per caricare correttamente il plugin
def setup(bot):
    bot.add_command(comandi)
