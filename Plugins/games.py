import discord
from discord.ext import commands
import random
import asyncio



#############################################
# Configurazione del Bot e degli Intent
#############################################

# Se il bot è già configurato nel file principale, questo plugin funziona in maniera autonoma.
intents = discord.Intents.default()
intents.message_content = True  # Necessario per leggere il contenuto dei messaggi
bot = commands.Bot(command_prefix='!', intents=intents)



#############################################
# Comandi per i Giochi
#############################################

@commands.command()
async def testa_o_croce(ctx):
    """Gioco del testa o croce: scegli testa o croce e vedi se hai indovinato."""
    # Genera casualmente "testa" o "croce"
    risultato = random.choice(['testa', 'croce'])
    await ctx.send("Scegli: testa o croce?")

    def check(message):
        return (message.author == ctx.author and 
                message.channel == ctx.channel and 
                message.content.lower() in ['testa', 'croce'])

    try:
        # Attende la risposta dell'utente con timeout di 30 secondi
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Tempo scaduto! Non hai risposto in tempo.")
        return

    # Determina il vincitore e mostra il risultato in un embed
    if msg.content.lower() == risultato:
        embed = discord.Embed(
            title="Testa o Croce",
            description=f"È uscito **{risultato}**! Hai vinto!",
            color=0x00ff00
        )
    else:
        embed = discord.Embed(
            title="Testa o Croce",
            description=f"È uscito **{risultato}**! Hai perso!",
            color=0xff5555
        )
    await ctx.send(embed=embed)

@commands.command()
async def indovina(ctx):
    """Gioco del numero casuale: prova a indovinare un numero tra 1 e 10."""
    numero = random.randint(1, 10)
    await ctx.send("Indovina il numero tra 1 e 10!")

    def check(message):
        return (message.author == ctx.author and 
                message.channel == ctx.channel and 
                message.content.isdigit())

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Tempo scaduto! Non hai risposto in tempo.")
        return

    if int(msg.content) == numero:
        embed = discord.Embed(
            title="Indovina il Numero",
            description=f"Hai indovinato il numero **{numero}**!",
            color=0x43b581
        )
    else:
        embed = discord.Embed(
            title="Indovina il Numero",
            description=f"Hai sbagliato! Il numero giusto era **{numero}**.",
            color=0xff5555
        )
    await ctx.send(embed=embed)



#############################################
# Setup del plugin Games
#############################################
def setup(bot):
    bot.add_command(testa_o_croce)
    bot.add_command(indovina)
