import discord
from discord.ext import commands



#############################################
# Configurazione del Bot e degli Intent
#############################################
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)



#############################################
# Comandi per la gestione del Server
#############################################

@commands.command()
async def server(ctx):
    """Mostra informazioni sul server."""
    guild = ctx.guild
    embed = discord.Embed(title=f"Informazioni su {guild.name}", color=0x00ff00)
    embed.add_field(name="ID", value=guild.id, inline=False)
    embed.add_field(name="Creato il", value=discord.utils.format_dt(guild.created_at, style='F'), inline=False)
    embed.add_field(name="Membri", value=guild.member_count, inline=False)
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

@commands.command()
async def role(ctx, action: str, role: discord.Role = None):
    # Verifica i permessi dell'utente
    if not ctx.author.guild_permissions.manage_roles:
        return await ctx.send("Non hai i permessi necessari per gestire i ruoli.")
    
    # Se l'azione è "list", invia la lista dei ruoli disponibili
    if action.lower() == "list":
        roles = [r.name for r in ctx.guild.roles]
        await ctx.send("Ruoli disponibili:\n" + "\n".join(roles))
        return

    # Per "add" e "remove" è necessario specificare un ruolo
    if role is None:
        return await ctx.send("Devi specificare un ruolo per questa azione.")

    # Azioni add/remove
    if action.lower() == "add":
        await ctx.author.add_roles(role)
        await ctx.send(f"Ruolo {role.mention} aggiunto a {ctx.author.mention}.")
    elif action.lower() == "remove":
        await ctx.author.remove_roles(role)
        await ctx.send(f"Ruolo {role.mention} rimosso da {ctx.author.mention}.")
    else:
        await ctx.send("Azione non valida. Usa `add`, `remove` o `list`.")

@commands.command()
async def clear(ctx, amount: int):
    """Pulisce un certo numero di messaggi nel canale corrente."""
    if ctx.author.guild_permissions.manage_messages:
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Ho cancellato {len(deleted)-1} messaggi.", delete_after=5)
    else:
        await ctx.send("Non hai i permessi necessari per cancellare i messaggi.")



#############################################
# Setup del plugin Server
#############################################
def setup(bot):
    bot.add_command(server)
    bot.add_command(role)
    bot.add_command(clear)
