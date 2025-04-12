import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ---------------------------------------
# Comandi per la gestione del Server
# ---------------------------------------


@commands.command()
async def server(ctx):
    """Mostra informazioni sul server."""
    server = ctx.guild
    embed = discord.Embed(title=f"Informazioni su {server.name}", color=0x00ff00)
    embed.add_field(name="ID", value=server.id, inline=False)
    embed.add_field(name="Creato il", value=discord.utils.format_dt(server.created_at), inline=False)
    embed.add_field(name="Membri", value=server.member_count, inline=False)
    embed.set_thumbnail(url=server.icon_url)
    await ctx.send(embed=embed)


@commands.command()
async def role(ctx, action: str, role_id: discord.Role):
    """Aggiunge o rimuove un ruolo."""
    if ctx.author.guild_permissions.manage_roles:
        role = discord.utils.get(ctx.guild.roles, name="role_id")

        if action == "add":
            await ctx.author.add_roles(role)
            await ctx.send(f"Ruolo aggiunto a {ctx.author.mention}")

        elif action == "remove":
            await ctx.author.remove_roles(role)
            await ctx.send(f"Ruolo rimosso a {ctx.author.mention}")

        else:
            await ctx.send("Azione non valida. Usa 'add' o 'remove'.")

    else:
        await ctx.send("Non hai i permessi necessari")

    """Invia la lista dei ruoli disponibili."""
    if action == "list":
        roles = [role.name for role in ctx.guild.roles]
        await ctx.send("Ruoli disponibili:\n" + "\n".join(roles))


@commands.command()
async def clear(ctx, amount: int):
    """Pulisce un certo numero di messaggi."""
    if ctx.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Ho cancellato {amount} messaggi.", delete_after=5)
    else:
        await ctx.send("Non hai i permessi necessari.")





# La funzione setup è necessaria per caricare correttamente il plugin
def setup(bot):
    bot.add_command(server)
    bot.add_command(role)
    bot.add_command(clear)
