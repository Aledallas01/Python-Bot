import discord
from discord.ext import commands

#############################################
# Configurazione del Bot e costanti
#############################################
# Se hai configurato gli intents nel file principale, questo è un plugin standalone.
# Il prefisso usato per i comandi (qui ne usiamo uno fisso per la formattazione, non per la creazione dei comandi)
PREFIX = "!"
# Dizionario dei comandi con le loro descrizioni
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

#############################################
# Helper: Crea un embed standardizzato
#############################################
def create_embed(title: str, description: str, color: int = 0x00ff00):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="Usa !comandi per visualizzare questa lista.")
    return embed

#############################################
# Comando !comandi: visualizza la lista dei comandi disponibili
#############################################
@commands.command()
async def comandi(ctx):
    help_message = "Ecco la lista dei comandi disponibili:\n"
    # Crea un embed usando il helper, con titolo e colore personalizzato
    embed = create_embed("Comandi disponibili", help_message, color=0x00ff00)
    
    # Aggiunge ogni comando come campo nell'embed (non inline per maggiore leggibilità)
    for comando, descrizione in COMANDI.items():
        embed.add_field(name=f"{PREFIX}{comando}", value=descrizione, inline=False)
    
    # Manda l'embed come risposta
    await ctx.send(embed=embed)



#############################################
# Setup del plugin comandi
#############################################
def setup(bot):
    bot.add_command(comandi)
