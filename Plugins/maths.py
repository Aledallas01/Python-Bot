import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ---------------------------------------
# Comandi per la matematica
# ---------------------------------------

@commands.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@commands.command()
async def sub(ctx, left: int, right: int):
    """Subtracts two numbers."""
    await ctx.send(left - right)


@commands.command()
async def mul(ctx, left: int, right: int):
    """Multiplies two numbers."""
    await ctx.send(left * right)


@commands.command()
async def div(ctx, left: int, right: int):
    """Divides two numbers."""
    await ctx.send(left / right)


# La funzione setup è necessaria per caricare correttamente il plugin
def setup(bot):
    bot.add_command(add)
    bot.add_command(sub)
    bot.add_command(mul)
    bot.add_command(div)
