import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ---------------------------------------
# Comandi base
# ---------------------------------------

@commands.command()
async def ciao(ctx):
    """Comando per salutare."""
    await ctx.send(f'Ciao! Sono un bot {bot.user}!')


@commands.command()
async def arrivederci(ctx):
    """Comando per salutare."""
    await ctx.send("Arrivederci!")


@commands.command()
async def password(ctx, larghezza: int):
    """Genera una password casuale."""
    elements = '+-/*!&$#?=@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    for i in range (larghezza):
        password = password + random.choice(elements)
    embed = discord.Embed(title = "Password", description = "Questa è la tua password", color=0x00ff00)
    embed.add_field(name=f"La tua password è: {password}", value ="", inline=False)

    await ctx.send(embed=embed)


# La funzione setup è necessaria per caricare correttamente il plugin
def setup(bot):
    bot.add_command(ciao)
    bot.add_command(arrivederci)
    bot.add_command(password)
