import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

GUILD_ID = 1354841382916718744       # ID del Server
OWNER_ROLE_ID = 1354852422916243700    # ID del ruolo OWNER
STAFF_ROLE_ID = 1355235876942250120    # ID del ruolo STAFF
MUTED_ROLE_ID = 1354911951649767514    # ID del ruolo Muted


# ---------------------------------------
# Comandi per la gestione degli utenti
# ---------------------------------------

@commands.command()
async def joined(ctx, member: discord.Member):
    """Dice quando un membro è entrato nel server."""
    # Usa discord.utils.format_dt per formattare la data di joined
    join_date = discord.utils.format_dt(member.joined_at, style="F")
    await ctx.send(f'{member.name} è entrato nel server il {join_date}.')

@commands.command()
async def role_add(ctx, member: discord.Member, role: discord.Role):
    """Aggiunge (o rimuove se già presente) un ruolo a un membro."""
    if ctx.author.guild_permissions.manage_roles:
        # Usa il ruolo passato come parametro, non una stringa fissa
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"Ruolo rimosso da {member.mention}.")
        else:
            await member.add_roles(role)
            await ctx.send(f"Ruolo aggiunto a {member.mention}.")
    else:
        await ctx.send("Non hai i permessi necessari.")

@commands.command()
async def online(ctx):
    """Mostra i membri online."""
    online_members = [member.name for member in ctx.guild.members if member.status == discord.Status.online]
    if online_members:
        await ctx.send("Membri online:\n" + "\n".join(online_members))
    else:
        await ctx.send("Nessun membro online al momento.")

@commands.command()
async def offline(ctx):
    """Mostra i membri offline."""
    offline_members = [member.name for member in ctx.guild.members if member.status == discord.Status.offline]
    if offline_members:
        await ctx.send("Membri offline:\n" + "\n".join(offline_members))
    else:
        await ctx.send("Nessun membro offline al momento.")

@commands.command()
async def ban(ctx, member: discord.Member):
    """Banna un membro."""
    if ctx.author.guild_permissions.ban_members:
        await member.ban()
        await ctx.send(f"{member.name} è stato bannato.")
    else:
        await ctx.send("Non hai i permessi necessari per bannare membri.")

@commands.command()
async def unban(ctx, member: discord.Member):
    """Unbanna un membro."""
    if ctx.author.guild_permissions.ban_members:
        await member.unban()
        await ctx.send(f"{member.name} è stato unbannato.")
    else:
        await ctx.send("Non hai i permessi necessari per unban.")

@commands.command()
async def kick(ctx, member: discord.Member):
    """Espelle un membro."""
    if ctx.author.guild_permissions.kick_members:
        await member.kick()
        await ctx.send(f"{member.name} è stato espulso.")
    else:
        await ctx.send("Non hai i permessi necessari per espellere membri.")

@commands.command()
async def mute(ctx, member: discord.Member):
    """Muta un membro."""
    if ctx.author.guild_permissions.mute_members:
        # Assumendo che MUTED_ROLE_ID sia una variabile numerica, cerca il ruolo per ID
        role = discord.utils.get(ctx.guild.roles, id=MUTED_ROLE_ID)
        if role:
            await member.add_roles(role)
            await ctx.send(f"{member.name} è stato mutato.")
        else:
            await ctx.send("Ruolo 'Muted' non trovato.")
    else:
        await ctx.send("Non hai i permessi necessari per mutare membri.")

@commands.command()
async def unmute(ctx, member: discord.Member):
    """Unmuta un membro."""
    if ctx.author.guild_permissions.mute_members:
        role = discord.utils.get(ctx.guild.roles, id=MUTED_ROLE_ID)
        if role:
            await member.remove_roles(role)
            await ctx.send(f"{member.name} è stato unmutato.")
        else:
            await ctx.send("Ruolo 'Muted' non trovato.")
    else:
        await ctx.send("Non hai i permessi necessari per unmutare membri.")

# La funzione setup è necessaria per caricare correttamente il plugin
def setup(bot):
    bot.add_command(joined)
    bot.add_command(role_add)
    bot.add_command(online)
    bot.add_command(offline)
    bot.add_command(ban)
    bot.add_command(unban)
    bot.add_command(kick)
    bot.add_command(mute)
    bot.add_command(unmute)
