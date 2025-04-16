import discord
from discord.ext import commands

#############################################
# Configurazione del Bot e costanti
#############################################
# Se il bot è già configurato nel file principale, questo plugin funge in maniera autonoma.
intents = discord.Intents.default()
intents.message_content = True  # Consente l'accesso al contenuto dei messaggi
bot = commands.Bot(command_prefix='!', intents=intents)

# Costanti (modifica gli ID in base al tuo server)
GUILD_ID = 0000000000000000000       # ID del Server
OWNER_ROLE_ID = 0000000000000000000    # ID del ruolo OWNER
STAFF_ROLE_ID = 0000000000000000000    # ID del ruolo STAFF
MUTED_ROLE_ID = 0000000000000000000    # ID del ruolo Muted



#############################################
# Comandi per la gestione degli utenti
#############################################

@commands.command()
async def joined(ctx, member: discord.Member):
    join_date = discord.utils.format_dt(member.joined_at, style="F")
    await ctx.send(f'{member.name} è entrato nel server il {join_date}.')

@commands.command()
async def role_add(ctx, member: discord.Member, role: discord.Role):
    if ctx.author.guild_permissions.manage_roles:
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.send(f"Ruolo {role.mention} rimosso da {member.mention}.")
        else:
            await member.add_roles(role)
            await ctx.send(f"Ruolo {role.mention} aggiunto a {member.mention}.")
    else:
        await ctx.send("Non hai i permessi necessari per gestire i ruoli.")

@commands.command()
async def online(ctx):
    online_members = [member.name for member in ctx.guild.members if member.status == discord.Status.online]
    if online_members:
        await ctx.send("Membri online:\n" + "\n".join(online_members))
    else:
        await ctx.send("Nessun membro online al momento.")

@commands.command()
async def offline(ctx):
    offline_members = [member.name for member in ctx.guild.members if member.status == discord.Status.offline]
    if offline_members:
        await ctx.send("Membri offline:\n" + "\n".join(offline_members))
    else:
        await ctx.send("Nessun membro offline al momento.")

@commands.command()
async def ban(ctx, member: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        try:
            await member.ban()
            await ctx.send(f"{member.name} è stato bannato.")
        except Exception as e:
            await ctx.send(f"Si è verificato un errore: {e}")
    else:
        await ctx.send("Non hai i permessi necessari per bannare membri.")

@commands.command()
async def unban(ctx, member: discord.Member):
    if ctx.author.guild_permissions.ban_members:
        try:
            await member.unban()
            await ctx.send(f"{member.name} è stato unbannato.")
        except Exception as e:
            await ctx.send(f"Si è verificato un errore: {e}")
    else:
        await ctx.send("Non hai i permessi necessari per unbannare membri.")

@commands.command()
async def kick(ctx, member: discord.Member):
    if ctx.author.guild_permissions.kick_members:
        try:
            await member.kick()
            await ctx.send(f"{member.name} è stato espulso.")
        except Exception as e:
            await ctx.send(f"Si è verificato un errore: {e}")
    else:
        await ctx.send("Non hai i permessi necessari per espellere membri.")

@commands.command()
async def mute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.mute_members:
        role = discord.utils.get(ctx.guild.roles, id=MUTED_ROLE_ID)
        if role:
            try:
                await member.add_roles(role)
                await ctx.send(f"{member.name} è stato mutato.")
            except Exception as e:
                await ctx.send(f"Errore: {e}")
        else:
            await ctx.send("Ruolo 'Muted' non trovato.")
    else:
        await ctx.send("Non hai i permessi necessari per mutare membri.")

@commands.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.mute_members:
        role = discord.utils.get(ctx.guild.roles, id=MUTED_ROLE_ID)
        if role:
            try:
                await member.remove_roles(role)
                await ctx.send(f"{member.name} è stato unmutato.")
            except Exception as e:
                await ctx.send(f"Errore: {e}")
        else:
            await ctx.send("Ruolo 'Muted' non trovato.")
    else:
        await ctx.send("Non hai i permessi necessari per unmutare membri.")



#############################################
# Setup del plugin Users
#############################################
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
