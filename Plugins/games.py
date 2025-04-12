import discord
from discord.ext import commands
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ---------------------------------------
# Comandi per i giochi
# ---------------------------------------

#testa o croce migliorato
@commands.command()
async def testa_o_croce(ctx):
    """Gioco del testa o croce."""
    # Genera casualmente testa o croce
    risultato = random.choice(['testa', 'croce'])
    
    # Chiede all'utente di scegliere
    await ctx.send("Scegli: testa o croce?")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['testa', 'croce']

    try:
        # Attende la risposta dell'utente
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Tempo scaduto! Non hai risposto in tempo.")
        return

    # Determina il vincitore
    if msg.content.lower() == risultato:
        await ctx.send(f"È uscito {risultato}! Hai vinto!")
    else:
        await ctx.send(f"È uscito {risultato}! Hai perso!")


# gioco del numero casuale
@commands.command()
async def indovina(ctx):
    """Gioco del numero casuale."""
    numero = random.randint(1, 10)
    await ctx.send("Indovina il numero tra 1 e 10!")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send("Tempo scaduto! Non hai risposto in tempo.")
        return

    if int(msg.content) == numero:
        await ctx.send("Hai indovinato!")
    else:
        await ctx.send(f"Hai perso! Il numero era {numero}.")


# La funzione setup è necessaria per caricare correttamente il plugin
def setup(bot):
    bot.add_command(testa_o_croce)
    bot.add_command(indovina)
