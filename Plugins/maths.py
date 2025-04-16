import discord
from discord.ext import commands

#############################################
# Configurazione del Bot e degli Intent
#############################################
# Se il bot viene configurato nel file principale, questo plugin funziona in maniera autonoma.
intents = discord.Intents.default()
intents.message_content = True  # Necessario per leggere il contenuto dei messaggi
bot = commands.Bot(command_prefix='!', intents=intents)
NAME = "Dallas Bot"  # Nome del bot



#############################################
# Helper: Creazione di Embed Standardizzati
#############################################
def create_embed(title: str, description: str, color: int = 0x7289da):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=f"Plugin Base - Powered by {NAME}")
    return embed



#############################################
# Comandi per la matematica
#############################################

@commands.command()
async def add(ctx, left: int, right: int):
    """Somma due numeri e visualizza il risultato."""
    result = left + right
    embed = create_embed("Addizione", f"{left} + {right} = **{result}**", color=0x00ff00)
    await ctx.send(embed=embed)

@commands.command()
async def sub(ctx, left: int, right: int):
    """Sottrae due numeri e visualizza il risultato."""
    result = left - right
    embed = create_embed("Sottrazione", f"{left} - {right} = **{result}**", color=0xff9900)
    await ctx.send(embed=embed)

@commands.command()
async def mul(ctx, left: int, right: int):
    """Moltiplica due numeri e visualizza il risultato."""
    result = left * right
    embed = create_embed("Moltiplicazione", f"{left} * {right} = **{result}**", color=0x7289da)
    await ctx.send(embed=embed)

@commands.command()
async def div(ctx, left: int, right: int):
    """Divide due numeri e visualizza il risultato."""
    try:
        # Protezione da divisione per zero
        result = left / right
        embed = create_embed("Divisione", f"{left} / {right} = **{result}**", color=0x00ccff)
    except ZeroDivisionError:
        embed = create_embed("Divisione", "Errore: divisione per zero non permessa!", color=0xff5555)
    await ctx.send(embed=embed)



#############################################
# Setup del plugin Maths
#############################################
def setup(bot):
    bot.add_command(add)
    bot.add_command(sub)
    bot.add_command(mul)
    bot.add_command(div)
