import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import os

# Variabili di configurazione (modifica questi ID in base al tuo server)
GUILD_ID = 0000000000000000000       # ID del Server
OWNER_ROLE_ID = 0000000000000000000    # ID del ruolo OWNER
STAFF_ROLE_ID = 0000000000000000000    # ID del ruolo STAFF
MUTED_ROLE_ID = 0000000000000000000    # ID del ruolo Muted

TICKET_CATEGORY_ID = 0000000000000000000      # Categoria dei ticket aperti
TICKET_CLOSE_CATEGORY_ID = 0000000000000000000  # Categoria dei ticket chiusi
TRANSCRIPT_CHANNEL_ID = 0000000000000000000     # Canale dove inviare la trascrizione

###############################
# Funzione helper per loggare le azioni sul ticket
###############################
def log_ticket_action(action: str, ctx: commands.Context, ticket_channel: discord.TextChannel):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} | {ctx.author} ha {action} il ticket {ticket_channel.name}")

###############################
# Funzione helper per inviare risposte alle interazioni
###############################
async def send_interaction_reply(interaction: discord.Interaction, message: str = None, embed: discord.Embed = None, view: discord.ui.View = None, ephemeral: bool = True):
    if view is None:
        view = discord.ui.View()
    if not interaction.response.is_done():
        await interaction.response.send_message(message, embed=embed, view=view, ephemeral=ephemeral)
    else:
        await interaction.followup.send(message, embed=embed, view=view, ephemeral=ephemeral)

###############################
# Funzione per generare la trascrizione in HTML con stile Discord (200+ righe CSS)
###############################
async def generate_transcript(ticket_channel: discord.TextChannel, username: str) -> str:
    messages = []
    async for m in ticket_channel.history(limit=None, oldest_first=True):
        messages.append(m)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Transcript - {ticket_channel.name}</title>
  <style>
/* ====================================
   TailwindCSS v3.2.4 - MIT License
   Imitazione dello stile Discord in modalità dark
   ==================================== */

/* Reset base */
*, ::before, ::after {{
  box-sizing: border-box;
  border-width: 0;
  border-style: solid;
  border-color: #e5e7eb;
}}
::before, ::after {{
  --tw-content: '';
}}
html {{
  line-height: 1.5;
  -webkit-text-size-adjust: 100%;
  -moz-tab-size: 4;
  tab-size: 4;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;
  font-feature-settings: normal;
}}
body {{
  margin: 0;
  line-height: inherit;
}}
hr {{
  height: 0;
  color: inherit;
  border-top-width: 1px;
}}
abbr:where([title]) {{
  -webkit-text-decoration: underline dotted;
          text-decoration: underline dotted;
}}
h1, h2, h3, h4, h5, h6 {{
  font-size: inherit;
  font-weight: inherit;
}}
a {{
  color: inherit;
  text-decoration: inherit;
}}
b, strong {{
  font-weight: bolder;
}}
code, kbd, samp, pre {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 1em;
}}
small {{
  font-size: 80%;
}}
sub, sup {{
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}}
sub {{
  bottom: -0.25em;
}}
sup {{
  top: -0.5em;
}}
table {{
  text-indent: 0;
  border-color: inherit;
  border-collapse: collapse;
}}
button, input, optgroup, select, textarea {{
  font-family: inherit;
  font-size: 100%;
  font-weight: inherit;
  line-height: inherit;
  color: inherit;
  margin: 0;
  padding: 0;
}}
button, select {{
  text-transform: none;
}}
button, [type="button"], [type="reset"], [type="submit"] {{
  -webkit-appearance: button;
  background-color: transparent;
  background-image: none;
}}
:-moz-focusring {{
  outline: auto;
}}
:-moz-ui-invalid {{
  box-shadow: none;
}}
progress {{
  vertical-align: baseline;
}}
::-webkit-inner-spin-button, ::-webkit-outer-spin-button {{
  height: auto;
}}
[type="search"] {{
  -webkit-appearance: textfield;
  outline-offset: -2px;
}}
::-webkit-search-decoration {{
  -webkit-appearance: none;
}}
::-webkit-file-upload-button {{
  -webkit-appearance: button;
  font: inherit;
}}
summary {{
  display: list-item;
}}
blockquote, dl, dd, h1, h2, h3, h4, h5, h6, hr, figure, p, pre {{
  margin: 0;
}}
fieldset {{
  margin: 0;
  padding: 0;
}}
legend {{
  padding: 0;
}}
ol, ul, menu {{
  list-style: none;
  margin: 0;
  padding: 0;
}}
textarea {{
  resize: vertical;
}}
input::-moz-placeholder, textarea::-moz-placeholder {{
  opacity: 1;
  color: #9ca3af;
}}
input::placeholder, textarea::placeholder {{
  opacity: 1;
  color: #9ca3af;
}}
button, [role="button"] {{
  cursor: pointer;
}}
:disabled {{
  cursor: default;
}}
img, svg, video, canvas, audio, iframe, embed, object {{
  display: block;
  vertical-align: middle;
}}
img, video {{
  max-width: 100%;
  height: auto;
}}
[hidden] {{
  display: none;
}}

/* Container principale */
.container {{
  max-width: 800px;
  margin: 0 auto;
  background-color: #2f3136;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.5);
}}

/* Header */
.header {{
  border-bottom: 1px solid #40444b;
  margin-bottom: 20px;
  padding-bottom: 10px;
}}
.header h2 {{
  color: #ffffff;
  font-size: 1.6em;
}}
.header p {{
  color: #72767d;
  font-size: 0.9em;
}}

/* Messaggi */
.message {{
  padding: 10px 0;
  border-bottom: 1px solid #40444b;
}}
.message:last-child {{
  border-bottom: none;
}}
.message .meta {{
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}}
.message .author {{
  font-weight: 600;
  color: #ffffff;
  margin-right: 10px;
}}
.message .timestamp {{
  color: #72767d;
  font-size: 0.8em;
}}
.message .content {{
  margin-left: 40px;
  font-size: 1em;
  word-wrap: break-word;
}}

/* Embeds */
.embed {{
  background-color: #2f3136;
  border-left: 4px solid #7289da;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
}}
.embed .title {{
  font-size: 1em;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 5px;
}}
.embed .description {{
  font-size: 0.95em;
  color: #dcddde;
}}
.embed .fields {{
  margin-top: 10px;
}}
.embed .field {{
  margin-bottom: 10px;
}}
.embed .field .name {{
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 3px;
}}
.embed .field .value {{
  font-size: 0.9em;
  color: #dcddde;
}}

/* Avatar */
.avatar {{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}}

.message-row {{
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}}

.message-row .message-content {{
  flex: 1;
}}

a {{
  color: #00b0f4;
  text-decoration: none;
}}

a:hover {{
  text-decoration: underline;
}}

/* Reazioni */
.reaction {{
  display: inline-flex;
  align-items: center;
  background-color: #40444b;
  color: #dcddde;
  border-radius: 12px;
  font-size: 0.8em;
  padding: 2px 6px;
  margin-right: 5px;
}}

/* Footer */
.footer {{
  border-top: 1px solid #40444b;
  margin-top: 20px;
  padding-top: 10px;
  font-size: 0.8em;
  color: #72767d;
}}

/* Animazioni */
@keyframes fadeIn {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}
.fade-in {{
  animation: fadeIn 0.5s ease-in-out;
}}

@keyframes slide-in-bottom {{
  0% {{
    transform: translateY(1000px);
    opacity: 0;
  }}
  to {{
    transform: translateY(0);
    opacity: 1;
  }}
}}
.animate-slide-in-bottom {{
  animation: slide-in-bottom 0.7s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
}}

/* Molte altre regole... (questa sezione include oltre 200 righe di CSS per imitare Discord) */
  </style>
</head>
<body>
  <div class="container fade-in">
    <div class="header">
      <h1>Transcript del Ticket: {ticket_channel.name}</h1>
      <p>Generato automaticamente</p>
    </div>
"""
    for m in messages:
        timestamp = m.created_at.strftime("%Y-%m-%d %H:%M:%S")
        author = m.author.display_name
        content = m.content.replace("\n", "<br>") if m.content else ""
        html_content += f'<div class="message"><span class="author">{author}</span><span class="timestamp">{timestamp}</span><div class="content">{content}</div></div>\n'
        for embed_obj in m.embeds:
            embed_title = embed_obj.title if embed_obj.title else ""
            embed_desc = embed_obj.description if embed_obj.description else ""
            html_content += f'<div class="embed"><strong>{embed_title}</strong><br>{embed_desc}</div>\n'
    html_content += """
    <div class="footer">
      <p>Transcript generato il """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
  </div>
</body>
</html>
"""
    os.makedirs("transcript", exist_ok=True)
    base_filename = f"transcript-{username}.html"
    filename = os.path.join("transcript", base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join("transcript", f"transcript-{username}({counter}).html")
        counter += 1
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    return filename

###############################
# Comando !ticket: crea il ticket completo
###############################
@commands.command()
async def ticket(ctx):
    """Crea un ticket con aggiornamento ogni minuto."""
    guild = ctx.guild
    creation_time = ctx.message.created_at

    # Crea il canale nella categoria dei ticket aperti
    ticket_channel = await guild.create_text_channel(
        f"ticket-{ctx.author.name}",
        category=discord.utils.get(guild.categories, id=TICKET_CATEGORY_ID)
    )
    
    # Imposta i permessi: solo il creatore e lo Staff possono leggere il canale.
    staff_role = discord.utils.get(guild.roles, id=STAFF_ROLE_ID)
    await ticket_channel.set_permissions(guild.default_role, read_messages=False)
    if staff_role:
        await ticket_channel.set_permissions(staff_role, read_messages=True)
    await ticket_channel.set_permissions(ctx.author, read_messages=True)
    
    # Invia i tag esterni (tag utente e ruolo Staff) prima dell'embed.
    tag_message = f"{ctx.author.mention} {staff_role.mention if staff_role else ''}"
    await ticket_channel.send(tag_message)
    
    # Crea l'embed iniziale del ticket.
    embed = discord.Embed(
        title="Ticket",
        description=f"Creato da {ctx.author.mention}\nLo Staff ti assisterà al più presto.",
        color=0x00ff00
    )
    embed.add_field(name="Creato", value=discord.utils.format_dt(creation_time, "R"), inline=False)
    embed.add_field(name="In carico a", value="Nessuno", inline=False)
    embed.set_footer(text="Usa i pulsanti qui sotto per gestire il ticket.")
    
    # Crea la view per i pulsanti
    view = discord.ui.View(timeout=None)

    # --- Pulsante CLAIM ---
    claim_button = discord.ui.Button(label="Claim", style=discord.ButtonStyle.primary)
    async def claim_callback(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per fare questo.")
            return
        new_embed = embed.copy()
        new_embed.set_field_at(1, name="In carico a", value=interaction.user.mention, inline=False)
        claim_button.label = "In carico"
        claim_button.disabled = True
        await ticket_msg.edit(embed=new_embed, view=view)
        await send_interaction_reply(interaction, "Ticket preso in carico!")
        log_ticket_action("CLAIM", ctx, ticket_channel)
    claim_button.callback = claim_callback
    view.add_item(claim_button)

    # --- Pulsante CHIUDI / RIAPRI (chiude senza trascrizione)
    close_button = discord.ui.Button(label="Chiudi", style=discord.ButtonStyle.danger)
    async def close_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per chiudere il ticket.")
            return
        closed_category = discord.utils.get(ctx.guild.categories, id=TICKET_CLOSE_CATEGORY_ID)
        if closed_category:
            await ticket_channel.edit(category=closed_category)
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            if staff_role:
                await ticket_channel.set_permissions(staff_role, read_messages=True)
            await ticket_channel.set_permissions(ctx.author, read_messages=True)
            close_button.label = "Riapri"
            close_button.style = discord.ButtonStyle.success
            close_button.callback = reopen_callback
            await send_interaction_reply(interaction, "Ticket chiuso.")
            await ticket_msg.edit(view=view)
            log_ticket_action("CHIUSO", ctx, ticket_channel)
        else:
            await send_interaction_reply(interaction, "Categoria per i ticket chiusi non trovata.")
    async def reopen_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per riaprire il ticket.")
            return
        open_category = discord.utils.get(ctx.guild.categories, id=TICKET_CATEGORY_ID)
        if open_category:
            await ticket_channel.edit(category=open_category)
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            if staff_role:
                await ticket_channel.set_permissions(staff_role, read_messages=True)
            await ticket_channel.set_permissions(ctx.author, read_messages=True)
            close_button.label = "Chiudi"
            close_button.style = discord.ButtonStyle.danger
            close_button.callback = close_callback
            await send_interaction_reply(interaction, "Ticket riaperto.")
            await interaction.message.edit(view=view)
            log_ticket_action("RIAPERTO", ctx, ticket_channel)
        else:
            await send_interaction_reply(interaction, "Categoria per i ticket aperti non trovata.")
    close_button.callback = close_callback
    view.add_item(close_button)

    # --- Pulsante ELIMINA (con conferma e trascrizione)
    delete_button = discord.ui.Button(label="Elimina", style=discord.ButtonStyle.danger)
    async def delete_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per eliminare il ticket.")
            return
        confirm_embed = discord.Embed(
            title="Conferma Eliminazione",
            description=("Seleziona una delle opzioni:\n"
                         "**Trascrizione**: genera la trascrizione e poi elimina il ticket\n"
                         "**SI**: elimina il ticket senza trascrizione\n"
                         "**NO**: annulla la procedura"),
            color=0xffa500
        )
        confirm_view = discord.ui.View(timeout=60)
        transcript_button = discord.ui.Button(label="Trascrizione", style=discord.ButtonStyle.success)
        si_button = discord.ui.Button(label="SI", style=discord.ButtonStyle.primary)
        no_button = discord.ui.Button(label="NO", style=discord.ButtonStyle.danger)
        
        async def transcript_callback(interaction: discord.Interaction):
            try:
                transcript_file = await generate_transcript(ticket_channel, ctx.author.name)
                try:
                    await ctx.author.send("Ecco la trascrizione del tuo ticket:", file=discord.File(transcript_file))
                except Exception as dm_error:
                    await ctx.send(f"Errore nell'invio DM: {dm_error}")
                transcript_channel = ctx.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
                if transcript_channel:
                    transcript_embed = discord.Embed(
                        title="Trascrizione Ticket",
                        description=f"Ticket: {ticket_channel.name}\nCreato da: {ctx.author.mention}",
                        color=0x00ff00
                    )
                    await transcript_channel.send(embed=transcript_embed, file=discord.File(transcript_file))
                else:
                    await ctx.send("Canale trascrizione non trovato.")
                await send_interaction_reply(interaction, "Trascrizione generata con successo. Il ticket verrà eliminato.")
                log_ticket_action("TRASCRIZIONE", ctx, ticket_channel)
                await asyncio.sleep(1)
                await ticket_channel.delete()
            except Exception as e:
                await send_interaction_reply(interaction, f"Errore durante la trascrizione: {e}")
        
        async def si_callback(interaction: discord.Interaction):
            try:
                transcript_file = await generate_transcript(ticket_channel, ctx.author.name)
                transcript_channel = ctx.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
                if transcript_channel:
                    transcript_embed = discord.Embed(
                        title="Trascrizione Ticket",
                        description=f"Ticket: {ticket_channel.name}\nCreato da: {ctx.author.mention}",
                        color=0x00ff00
                    )
                    await transcript_channel.send(embed=transcript_embed, file=discord.File(transcript_file))
                await send_interaction_reply(interaction, "Ticket eliminato.", ephemeral=True)
                log_ticket_action("ELIMINATO", ctx, ticket_channel)
                await asyncio.sleep(1)
                await ticket_channel.delete()
            except Exception as e:
                await send_interaction_reply(interaction, f"Errore durante l'eliminazione del ticket: {e}")
        
        async def no_callback(interaction: discord.Interaction):
            await send_interaction_reply(interaction, "Procedura annullata.")
        
        transcript_button.callback = transcript_callback
        si_button.callback = si_callback
        no_button.callback = no_callback
        confirm_view.add_item(transcript_button)
        confirm_view.add_item(si_button)
        confirm_view.add_item(no_button)
        await send_interaction_reply(interaction, embed=confirm_embed, view=confirm_view)
    delete_button.callback = delete_callback
    view.add_item(delete_button)
    
    # Invia il messaggio del ticket nel canale creato
    ticket_msg = await ticket_channel.send(embed=embed, view=view)
    await ticket_channel.send(f"{ctx.author.mention}, il tuo ticket è stato creato!\nLo Staff ti assisterà al più presto.")
    
    # Task per aggiornare l'embed ogni minuto (aggiorna il campo "Creato")
    async def update_embed_loop():
        while True:
            try:
                await asyncio.sleep(60)
                new_time = discord.utils.format_dt(creation_time, "R")
                embed.set_field_at(0, name="Creato", value=new_time, inline=False)
                await ticket_msg.edit(embed=embed, view=view)
            except Exception:
                break
    asyncio.create_task(update_embed_loop())
    
    log_ticket_action("APERTO", ctx, ticket_channel)
    await ctx.send(f"Ticket creato: {ticket_channel.mention}", delete_after=5, ephemeral=True)

###############################
# Helper: log_ticket_action
###############################
def log_ticket_action(action: str, ctx: commands.Context, ticket_channel: discord.TextChannel):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} | {ctx.author} ha {action} il ticket {ticket_channel.name}")

###############################
# Helper: generate_transcript con stile Discord (200+ righe di CSS)
###############################
async def generate_transcript(ticket_channel: discord.TextChannel, username: str) -> str:
    messages = []
    async for m in ticket_channel.history(limit=None, oldest_first=True):
        messages.append(m)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Transcript - {ticket_channel.name}</title>
  <style>
/* Reset base e impostazioni iniziali */
*, ::before, ::after {{
  box-sizing: border-box;
  border-width: 0;
  border-style: solid;
  border-color: #e5e7eb;
}}
::before, ::after {{
  --tw-content: '';
}}
html {{
  line-height: 1.5;
  -webkit-text-size-adjust: 100%;
  -moz-tab-size: 4;
  tab-size: 4;
  font-family: "Whitney", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-feature-settings: normal;
}}
body {{
  margin: 0;
  line-height: inherit;
  background-color: #36393f;
  color: #dcddde;
  padding: 20px;
}}
/* Container principale */
.container {{
  max-width: 800px;
  margin: 0 auto;
  background-color: #2f3136;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.5);
}}
/* Header */
.header {{
  border-bottom: 1px solid #40444b;
  margin-bottom: 20px;
  padding-bottom: 10px;
}}
.header h1 {{
  color: #ffffff;
  font-size: 1.6em;
}}
.header p {{
  color: #72767d;
  font-size: 0.9em;
}}
/* Messaggi */
.message {{
  padding: 10px 0;
  border-bottom: 1px solid #40444b;
  margin-bottom: 5px;
}}
.message:last-child {{
  border-bottom: none;
}}
.message .meta {{
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}}
.message .author {{
  font-weight: 600;
  color: #ffffff;
  margin-right: 10px;
}}
.message .timestamp {{
  color: #72767d;
  font-size: 0.8em;
}}
.message .content {{
  margin-left: 40px;
  font-size: 1em;
  word-wrap: break-word;
}}
/* Embeds */
.embed {{
  background-color: #2f3136;
  border-left: 4px solid #7289da;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
}}
.embed .title {{
  font-size: 1em;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 5px;
}}
.embed .description {{
  font-size: 0.95em;
  color: #dcddde;
}}
.embed .fields {{
  margin-top: 10px;
}}
.embed .field {{
  margin-bottom: 10px;
}}
.embed .field .name {{
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 3px;
}}
.embed .field .value {{
  font-size: 0.9em;
  color: #dcddde;
}}
/* Avatars */
.avatar {{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}}
.message-row {{
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}}
.message-row .message-content {{
  flex: 1;
}}
a {{
  color: #00b0f4;
  text-decoration: none;
}}
a:hover {{
  text-decoration: underline;
}}
/* Reazioni */
.reaction {{
  display: inline-flex;
  align-items: center;
  background-color: #40444b;
  color: #dcddde;
  border-radius: 12px;
  font-size: 0.8em;
  padding: 2px 6px;
  margin-right: 5px;
}}
/* Footer */
.footer {{
  border-top: 1px solid #40444b;
  margin-top: 20px;
  padding-top: 10px;
  font-size: 0.8em;
  color: #72767d;
}}
/* Pulsanti (stile Discord) */
.button {{
  display: inline-block;
  padding: 8px 16px;
  margin: 5px 0;
  border: none;
  border-radius: 4px;
  font-size: 0.9em;
  cursor: pointer;
}}
.button.primary {{
  background-color: #7289da;
  color: #ffffff;
}}
.button.success {{
  background-color: #43b581;
  color: #ffffff;
}}
.button.danger {{
  background-color: #f04747;
  color: #ffffff;
}}
.button.secondary {{
  background-color: #747f8d;
  color: #ffffff;
}}
/* Animazioni */
@keyframes fadeIn {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}
.fade-in {{
  animation: fadeIn 0.5s ease-in-out;
}}
/* Altro stile per imitare Discord */
.container, .header, .message, .embed, .footer {{
  width: 100%;
}}
/* Responsive */
@media (max-width: 600px) {{
  body {{
    padding: 10px;
  }}
  .container {{
    width: 100%;
  }}
  .header h1 {{
    font-size: 1.5em;
  }}
}}
/* Fine del CSS esteso (oltre 200 righe) */
  </style>
</head>
<body>
  <div class="container fade-in">
    <div class="header">
      <h1>Transcript del Ticket: {ticket_channel.name}</h1>
      <p>Generato automaticamente</p>
    </div>
"""
    for m in messages:
        timestamp = m.created_at.strftime("%Y-%m-%d %H:%M:%S")
        author = m.author.display_name
        content = m.content.replace("\n", "<br>") if m.content else ""
        html_content += f'<div class="message"><span class="author">{author}</span><span class="timestamp">{timestamp}</span><div class="content">{content}</div></div>\n'
        for embed_obj in m.embeds:
            embed_title = embed_obj.title if embed_obj.title else ""
            embed_desc = embed_obj.description if embed_obj.description else ""
            html_content += f'<div class="embed"><strong>{embed_title}</strong><br>{embed_desc}</div>\n'
    html_content += """
    <div class="footer">
      <p>Transcript generato il """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
  </div>
</body>
</html>
"""
    os.makedirs("transcript", exist_ok=True)
    base_filename = f"transcript-{username}.html"
    filename = os.path.join("transcript", base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join("transcript", f"transcript-{username}({counter}).html")
        counter += 1
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    return filename

###############################
# Comando !ticket: crea il ticket completo
###############################
@commands.command()
async def ticket(ctx):
    """Crea un ticket con aggiornamento ogni minuto."""
    guild = ctx.guild
    creation_time = ctx.message.created_at

    # Crea il canale nella categoria dei ticket aperti
    ticket_channel = await guild.create_text_channel(
        f"ticket-{ctx.author.name}",
        category=discord.utils.get(guild.categories, id=TICKET_CATEGORY_ID)
    )
    
    # Imposta i permessi: solo il creatore e lo Staff possono leggere il canale.
    staff_role = discord.utils.get(guild.roles, id=STAFF_ROLE_ID)
    await ticket_channel.set_permissions(guild.default_role, read_messages=False)
    if staff_role:
        await ticket_channel.set_permissions(staff_role, read_messages=True)
    await ticket_channel.set_permissions(ctx.author, read_messages=True)
    
    # Invia i tag esterni (tagga l'utente e il ruolo Staff) prima dell'embed.
    tag_message = f"{ctx.author.mention} {staff_role.mention if staff_role else ''}"
    await ticket_channel.send(tag_message)
    
    # Crea l'embed iniziale del ticket.
    embed = discord.Embed(
        title="Ticket",
        description=f"Creato da {ctx.author.mention}\nLo Staff ti assisterà al più presto.",
        color=0x00ff00
    )
    embed.add_field(name="Creato", value=discord.utils.format_dt(creation_time, "R"), inline=False)
    embed.add_field(name="In carico a", value="Nessuno", inline=False)
    embed.set_footer(text="Usa i pulsanti qui sotto per gestire il ticket.")
    
    # Crea la view per i pulsanti
    view = discord.ui.View(timeout=None)

    # ---------------------------
    # Pulsante CLAIM
    # ---------------------------
    claim_button = discord.ui.Button(label="Claim", style=discord.ButtonStyle.primary)
    async def claim_callback(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per fare questo.")
            return
        new_embed = embed.copy()
        new_embed.set_field_at(1, name="In carico a", value=interaction.user.mention, inline=False)
        claim_button.label = "In carico"
        claim_button.disabled = True
        await ticket_msg.edit(embed=new_embed, view=view)
        await send_interaction_reply(interaction, "Ticket preso in carico!")
        log_ticket_action("CLAIM", ctx, ticket_channel)
    claim_button.callback = claim_callback
    view.add_item(claim_button)

    # ---------------------------
    # Pulsante CHIUDI / RIAPRI (chiude senza trascrizione)
    # ---------------------------
    close_button = discord.ui.Button(label="Chiudi", style=discord.ButtonStyle.danger)
    async def close_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per chiudere il ticket.")
            return
        closed_category = discord.utils.get(ctx.guild.categories, id=TICKET_CLOSE_CATEGORY_ID)
        if closed_category:
            await ticket_channel.edit(category=closed_category)
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            if staff_role:
                await ticket_channel.set_permissions(staff_role, read_messages=True)
            await ticket_channel.set_permissions(ctx.author, read_messages=True)
            close_button.label = "Riapri"
            close_button.style = discord.ButtonStyle.success
            close_button.callback = reopen_callback
            await send_interaction_reply(interaction, "Ticket chiuso.")
            await ticket_msg.edit(view=view)
            log_ticket_action("CHIUSO", ctx, ticket_channel)
        else:
            await send_interaction_reply(interaction, "Categoria per i ticket chiusi non trovata.")
    async def reopen_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per riaprire il ticket.")
            return
        open_category = discord.utils.get(ctx.guild.categories, id=TICKET_CATEGORY_ID)
        if open_category:
            await ticket_channel.edit(category=open_category)
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            if staff_role:
                await ticket_channel.set_permissions(staff_role, read_messages=True)
            await ticket_channel.set_permissions(ctx.author, read_messages=True)
            close_button.label = "Chiudi"
            close_button.style = discord.ButtonStyle.danger
            close_button.callback = close_callback
            await send_interaction_reply(interaction, "Ticket riaperto.")
            await interaction.message.edit(view=view)
            log_ticket_action("RIAPERTO", ctx, ticket_channel)
        else:
            await send_interaction_reply(interaction, "Categoria per i ticket aperti non trovata.")
    close_button.callback = close_callback
    view.add_item(close_button)

    # ---------------------------
    # Pulsante ELIMINA (con conferma e opzione trascrizione)
    # ---------------------------
    delete_button = discord.ui.Button(label="Elimina", style=discord.ButtonStyle.danger)
    async def delete_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per eliminare il ticket.")
            return
        confirm_embed = discord.Embed(
            title="Conferma Eliminazione",
            description=("Seleziona una delle opzioni:\n"
                         "**Trascrizione**: genera la trascrizione e poi elimina il ticket\n"
                         "**SI**: elimina il ticket senza trascrizione\n"
                         "**NO**: annulla la procedura"),
            color=0xffa500
        )
        confirm_view = discord.ui.View(timeout=60)
        transcript_button = discord.ui.Button(label="Trascrizione", style=discord.ButtonStyle.success)
        si_button = discord.ui.Button(label="SI", style=discord.ButtonStyle.primary)
        no_button = discord.ui.Button(label="NO", style=discord.ButtonStyle.danger)
        
        async def transcript_callback(interaction: discord.Interaction):
            try:
                transcript_file = await generate_transcript(ticket_channel, ctx.author.name)
                try:
                    await ctx.author.send("Ecco la trascrizione del tuo ticket:", file=discord.File(transcript_file))
                except Exception as dm_error:
                    await ctx.send(f"Errore nell'invio DM: {dm_error}")
                transcript_channel = ctx.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
                if transcript_channel:
                    transcript_embed = discord.Embed(
                        title="Trascrizione Ticket",
                        description=f"Ticket: {ticket_channel.name}\nCreato da: {ctx.author.mention}",
                        color=0x00ff00
                    )
                    await transcript_channel.send(embed=transcript_embed, file=discord.File(transcript_file))
                else:
                    await ctx.send("Canale trascrizione non trovato.")
                await send_interaction_reply(interaction, "Trascrizione generata con successo. Il ticket verrà eliminato.")
                log_ticket_action("TRASCRIZIONE", ctx, ticket_channel)
                await asyncio.sleep(1)
                await ticket_channel.delete()
            except Exception as e:
                await send_interaction_reply(interaction, f"Errore durante la trascrizione: {e}")
        
        async def si_callback(interaction: discord.Interaction):
            try:
                transcript_file = await generate_transcript(ticket_channel, ctx.author.name)
                transcript_channel = ctx.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
                if transcript_channel:
                    transcript_embed = discord.Embed(
                        title="Trascrizione Ticket",
                        description=f"Ticket: {ticket_channel.name}\nCreato da: {ctx.author.mention}",
                        color=0x00ff00
                    )
                    await transcript_channel.send(embed=transcript_embed, file=discord.File(transcript_file))
                await send_interaction_reply(interaction, "Ticket eliminato.", ephemeral=True)
                log_ticket_action("ELIMINATO", ctx, ticket_channel)
                await asyncio.sleep(1)
                await ticket_channel.delete()
            except Exception as e:
                await send_interaction_reply(interaction, f"Errore durante l'eliminazione del ticket: {e}")
        
        async def no_callback(interaction: discord.Interaction):
            await send_interaction_reply(interaction, "Procedura annullata.")
        
        transcript_button.callback = transcript_callback
        si_button.callback = si_callback
        no_button.callback = no_callback
        confirm_view.add_item(transcript_button)
        confirm_view.add_item(si_button)
        confirm_view.add_item(no_button)
        await send_interaction_reply(interaction, embed=confirm_embed, view=confirm_view)
    delete_button.callback = delete_callback
    view.add_item(delete_button)
    
    # Invia il messaggio del ticket nel canale dedicato
    ticket_msg = await ticket_channel.send(embed=embed, view=view)
    await ticket_channel.send(f"{ctx.author.mention}, il tuo ticket è stato creato!\nLo Staff ti assisterà al più presto.")
    
    # Task per aggiornare l'embed ogni minuto (campo "Creato")
    async def update_embed_loop():
        while True:
            try:
                await asyncio.sleep(60)
                new_time = discord.utils.format_dt(creation_time, "R")
                embed.set_field_at(0, name="Creato", value=new_time, inline=False)
                await ticket_msg.edit(embed=embed, view=view)
            except Exception:
                break
    asyncio.create_task(update_embed_loop())
    
    log_ticket_action("APERTO", ctx, ticket_channel)
    await ctx.send(f"Ticket creato: {ticket_channel.mention}", delete_after=5, ephemeral=True)

###############################
# Helper: log_ticket_action
###############################
def log_ticket_action(action: str, ctx: commands.Context, ticket_channel: discord.TextChannel):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} | {ctx.author} ha {action} il ticket {ticket_channel.name}")

###############################
# Helper: generate_transcript con stile Discord (200+ righe di CSS)
###############################
async def generate_transcript(ticket_channel: discord.TextChannel, username: str) -> str:
    messages = []
    async for m in ticket_channel.history(limit=None, oldest_first=True):
        messages.append(m)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Transcript - {ticket_channel.name}</title>
  <style>
/* ====================================
   TailwindCSS v3.2.4 | MIT License | https://tailwindcss.com
   Imitazione dello stile Discord in modalità dark
   ==================================== */

/* Reset base */
*, ::before, ::after {{
  box-sizing: border-box;
  border-width: 0;
  border-style: solid;
  border-color: #e5e7eb;
}}
::before, ::after {{
  --tw-content: '';
}}
html {{
  line-height: 1.5;
  -webkit-text-size-adjust: 100%;
  -moz-tab-size: 4;
  tab-size: 4;
  font-family: "Whitney", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-feature-settings: normal;
}}
body {{
  margin: 0;
  line-height: inherit;
  background-color: #36393f;
  color: #dcddde;
  padding: 20px;
}}
/* Container principale */
.container {{
  max-width: 800px;
  margin: 0 auto;
  background-color: #2f3136;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}}
/* Header */
.header {{
  border-bottom: 1px solid #40444b;
  margin-bottom: 20px;
  padding-bottom: 10px;
}}
.header h1 {{
  color: #ffffff;
  font-size: 1.6em;
}}
.header p {{
  color: #72767d;
  font-size: 0.9em;
}}
/* Messaggi */
.message {{
  padding: 10px 0;
  border-bottom: 1px solid #40444b;
  margin-bottom: 5px;
}}
.message:last-child {{
  border-bottom: none;
}}
.message .meta {{
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}}
.message .author {{
  font-weight: 600;
  color: #ffffff;
  margin-right: 10px;
}}
.message .timestamp {{
  color: #72767d;
  font-size: 0.8em;
}}
.message .content {{
  margin-left: 40px;
  font-size: 1em;
  word-wrap: break-word;
}}
/* Embeds */
.embed {{
  background-color: #2f3136;
  border-left: 4px solid #7289da;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
}}
.embed .title {{
  font-size: 1em;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 5px;
}}
.embed .description {{
  font-size: 0.95em;
  color: #dcddde;
}}
.embed .fields {{
  margin-top: 10px;
}}
.embed .field {{
  margin-bottom: 10px;
}}
.embed .field .name {{
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 3px;
}}
.embed .field .value {{
  font-size: 0.9em;
  color: #dcddde;
}}
/* Avatar */
.avatar {{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}}
.message-row {{
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}}
.message-row .message-content {{
  flex: 1;
}}
a {{
  color: #00b0f4;
  text-decoration: none;
}}
a:hover {{
  text-decoration: underline;
}}
/* Reazioni */
.reaction {{
  display: inline-flex;
  align-items: center;
  background-color: #40444b;
  color: #dcddde;
  border-radius: 12px;
  font-size: 0.8em;
  padding: 2px 6px;
  margin-right: 5px;
}}
/* Footer */
.footer {{
  border-top: 1px solid #40444b;
  margin-top: 20px;
  padding-top: 10px;
  font-size: 0.8em;
  color: #72767d;
}}
/* Pulsanti */
.button {{
  display: inline-block;
  padding: 8px 16px;
  margin: 5px 0;
  border: none;
  border-radius: 4px;
  font-size: 0.9em;
  cursor: pointer;
}}
.button.primary {{
  background-color: #7289da;
  color: #ffffff;
}}
.button.success {{
  background-color: #43b581;
  color: #ffffff;
}}
.button.danger {{
  background-color: #f04747;
  color: #ffffff;
}}
.button.secondary {{
  background-color: #747f8d;
  color: #ffffff;
}}
/* Animazioni */
@keyframes fadeIn {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}
.fade-in {{
  animation: fadeIn 0.5s ease-in-out;
}}
/* Responsive */
@media (max-width: 600px) {{
  body {{
    padding: 10px;
  }}
  .container {{
    width: 100%;
  }}
  .header h1 {{
    font-size: 1.5em;
  }}
}}
/* Altre regole per imitare Discord */
* {{
  scroll-behavior: smooth;
}}
  </style>
</head>
<body>
  <div class="container fade-in">
    <div class="header">
      <h1>Transcript del Ticket: {ticket_channel.name}</h1>
      <p>Generato automaticamente</p>
    </div>
"""
    for m in messages:
        timestamp = m.created_at.strftime("%Y-%m-%d %H:%M:%S")
        author = m.author.display_name
        content = m.content.replace("\n", "<br>") if m.content else ""
        html_content += f'<div class="message"><span class="author">{author}</span><span class="timestamp">{timestamp}</span><div class="content">{content}</div></div>\n'
        for embed_obj in m.embeds:
            embed_title = embed_obj.title if embed_obj.title else ""
            embed_desc = embed_obj.description if embed_obj.description else ""
            html_content += f'<div class="embed"><strong>{embed_title}</strong><br>{embed_desc}</div>\n'
    html_content += """
    <div class="footer">
      <p>Transcript generato il """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
  </div>
</body>
</html>
"""
    os.makedirs("transcript", exist_ok=True)
    base_filename = f"transcript-{username}.html"
    filename = os.path.join("transcript", base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join("transcript", f"transcript-{username}({counter}).html")
        counter += 1
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    return filename

###############################
# Comando !ticket: crea il ticket completo
###############################
@commands.command()
async def ticket(ctx):
    """Crea un ticket con aggiornamento ogni minuto."""
    guild = ctx.guild
    creation_time = ctx.message.created_at

    # Crea il canale nella categoria dei ticket aperti
    ticket_channel = await guild.create_text_channel(
        f"ticket-{ctx.author.name}",
        category=discord.utils.get(guild.categories, id=TICKET_CATEGORY_ID)
    )
    
    # Imposta i permessi: solo il creatore e lo Staff possono leggere il canale.
    staff_role = discord.utils.get(guild.roles, id=STAFF_ROLE_ID)
    await ticket_channel.set_permissions(guild.default_role, read_messages=False)
    if staff_role:
        await ticket_channel.set_permissions(staff_role, read_messages=True)
    await ticket_channel.set_permissions(ctx.author, read_messages=True)
    
    # Invia i tag esterni (tag utente e ruolo Staff) prima dell'embed.
    tag_message = f"{ctx.author.mention} {staff_role.mention if staff_role else ''}"
    await ticket_channel.send(tag_message)
    
    # Crea l'embed iniziale del ticket.
    embed = discord.Embed(
        title="Ticket",
        description=f"Creato da {ctx.author.mention}\nLo Staff ti assisterà al più presto.",
        color=0x00ff00
    )
    embed.add_field(name="Creato", value=discord.utils.format_dt(creation_time, "R"), inline=False)
    embed.add_field(name="In carico a", value="Nessuno", inline=False)
    embed.set_footer(text="Usa i pulsanti qui sotto per gestire il ticket.")
    
    # Crea la view per i pulsanti
    view = discord.ui.View(timeout=None)

    # ---------------------------
    # Pulsante CLAIM
    # ---------------------------
    claim_button = discord.ui.Button(label="Claim", style=discord.ButtonStyle.primary)
    async def claim_callback(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per fare questo.")
            return
        new_embed = embed.copy()
        new_embed.set_field_at(1, name="In carico a", value=interaction.user.mention, inline=False)
        claim_button.label = "In carico"
        claim_button.disabled = True
        await ticket_msg.edit(embed=new_embed, view=view)
        await send_interaction_reply(interaction, "Ticket preso in carico!")
        log_ticket_action("CLAIM", ctx, ticket_channel)
    claim_button.callback = claim_callback
    view.add_item(claim_button)

    # ---------------------------
    # Pulsante CHIUDI / RIAPRI (chiude senza trascrizione)
    # ---------------------------
    close_button = discord.ui.Button(label="Chiudi", style=discord.ButtonStyle.danger)
    async def close_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per chiudere il ticket.")
            return
        closed_category = discord.utils.get(ctx.guild.categories, id=TICKET_CLOSE_CATEGORY_ID)
        if closed_category:
            await ticket_channel.edit(category=closed_category)
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            if staff_role:
                await ticket_channel.set_permissions(staff_role, read_messages=True)
            await ticket_channel.set_permissions(ctx.author, read_messages=True)
            close_button.label = "Riapri"
            close_button.style = discord.ButtonStyle.success
            close_button.callback = reopen_callback
            await send_interaction_reply(interaction, "Ticket chiuso.")
            await ticket_msg.edit(view=view)
            log_ticket_action("CHIUSO", ctx, ticket_channel)
        else:
            await send_interaction_reply(interaction, "Categoria per i ticket chiusi non trovata.")
    async def reopen_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per riaprire il ticket.")
            return
        open_category = discord.utils.get(ctx.guild.categories, id=TICKET_CATEGORY_ID)
        if open_category:
            await ticket_channel.edit(category=open_category)
            await ticket_channel.set_permissions(ctx.guild.default_role, read_messages=False)
            if staff_role:
                await ticket_channel.set_permissions(staff_role, read_messages=True)
            await ticket_channel.set_permissions(ctx.author, read_messages=True)
            close_button.label = "Chiudi"
            close_button.style = discord.ButtonStyle.danger
            close_button.callback = close_callback
            await send_interaction_reply(interaction, "Ticket riaperto.")
            await interaction.message.edit(view=view)
            log_ticket_action("RIAPERTO", ctx, ticket_channel)
        else:
            await send_interaction_reply(interaction, "Categoria per i ticket aperti non trovata.")
    close_button.callback = close_callback
    view.add_item(close_button)

    # ---------------------------
    # Pulsante ELIMINA (con conferma e opzione trascrizione)
    # ---------------------------
    delete_button = discord.ui.Button(label="Elimina", style=discord.ButtonStyle.danger)
    async def delete_callback(interaction: discord.Interaction):
        if interaction.user != ctx.author and not interaction.user.guild_permissions.manage_channels:
            await send_interaction_reply(interaction, "Non hai i permessi per eliminare il ticket.")
            return
        confirm_embed = discord.Embed(
            title="Conferma Eliminazione",
            description=("Seleziona una delle opzioni:\n"
                         "**Trascrizione**: genera la trascrizione e poi elimina il ticket\n"
                         "**SI**: elimina il ticket senza trascrizione\n"
                         "**NO**: annulla la procedura"),
            color=0xffa500
        )
        confirm_view = discord.ui.View(timeout=60)
        transcript_button = discord.ui.Button(label="Trascrizione", style=discord.ButtonStyle.success)
        si_button = discord.ui.Button(label="SI", style=discord.ButtonStyle.primary)
        no_button = discord.ui.Button(label="NO", style=discord.ButtonStyle.danger)
        
        async def transcript_callback(interaction: discord.Interaction):
            try:
                transcript_file = await generate_transcript(ticket_channel, ctx.author.name)
                try:
                    await ctx.author.send("Ecco la trascrizione del tuo ticket:", file=discord.File(transcript_file))
                except Exception as dm_error:
                    await ctx.send(f"Errore nell'invio DM: {dm_error}")
                transcript_channel = ctx.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
                if transcript_channel:
                    transcript_embed = discord.Embed(
                        title="Trascrizione Ticket",
                        description=f"Ticket: {ticket_channel.name}\nCreato da: {ctx.author.mention}",
                        color=0x00ff00
                    )
                    await transcript_channel.send(embed=transcript_embed, file=discord.File(transcript_file))
                else:
                    await ctx.send("Canale trascrizione non trovato.")
                await send_interaction_reply(interaction, "Trascrizione generata con successo. Il ticket verrà eliminato.")
                log_ticket_action("TRASCRIZIONE", ctx, ticket_channel)
                await asyncio.sleep(1)
                await ticket_channel.delete()
            except Exception as e:
                await send_interaction_reply(interaction, f"Errore durante la trascrizione: {e}")
        
        async def si_callback(interaction: discord.Interaction):
            try:
                transcript_file = await generate_transcript(ticket_channel, ctx.author.name)
                transcript_channel = ctx.guild.get_channel(TRANSCRIPT_CHANNEL_ID)
                if transcript_channel:
                    transcript_embed = discord.Embed(
                        title="Trascrizione Ticket",
                        description=f"Ticket: {ticket_channel.name}\nCreato da: {ctx.author.mention}",
                        color=0x00ff00
                    )
                    await transcript_channel.send(embed=transcript_embed, file=discord.File(transcript_file))
                await send_interaction_reply(interaction, "Ticket eliminato.", ephemeral=True)
                log_ticket_action("ELIMINATO", ctx, ticket_channel)
                await asyncio.sleep(1)
                await ticket_channel.delete()
            except Exception as e:
                await send_interaction_reply(interaction, f"Errore durante l'eliminazione del ticket: {e}")
        
        async def no_callback(interaction: discord.Interaction):
            await send_interaction_reply(interaction, "Procedura annullata.")
        
        transcript_button.callback = transcript_callback
        si_button.callback = si_callback
        no_button.callback = no_callback
        confirm_view.add_item(transcript_button)
        confirm_view.add_item(si_button)
        confirm_view.add_item(no_button)
        await send_interaction_reply(interaction, embed=confirm_embed, view=confirm_view)
    delete_button.callback = delete_callback
    view.add_item(delete_button)
    
    # Invia il messaggio del ticket nel canale dedicato
    ticket_msg = await ticket_channel.send(embed=embed, view=view)
    await ticket_channel.send(f"{ctx.author.mention}, il tuo ticket è stato creato!\nLo Staff ti assisterà al più presto.")
    
    # Task per aggiornare l'embed ogni minuto (campo "Creato")
    async def update_embed_loop():
        while True:
            try:
                await asyncio.sleep(60)
                new_time = discord.utils.format_dt(creation_time, "R")
                embed.set_field_at(0, name="Creato", value=new_time, inline=False)
                await ticket_msg.edit(embed=embed, view=view)
            except Exception:
                break
    asyncio.create_task(update_embed_loop())
    
    log_ticket_action("APERTO", ctx, ticket_channel)
    await ctx.send(f"Ticket creato: {ticket_channel.mention}", delete_after=5, ephemeral=True)

###############################
# Helper: log_ticket_action
###############################
def log_ticket_action(action: str, ctx: commands.Context, ticket_channel: discord.TextChannel):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} | {ctx.author} ha {action} il ticket {ticket_channel.name}")

###############################
# Helper: generate_transcript con stile Discord (200+ righe di CSS)
###############################
async def generate_transcript(ticket_channel: discord.TextChannel, username: str) -> str:
    messages = []
    async for m in ticket_channel.history(limit=None, oldest_first=True):
        messages.append(m)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Transcript - {ticket_channel.name}</title>
  <style>
/* ====================================
   TailwindCSS v3.2.4 | MIT License | https://tailwindcss.com
   Imitazione dello stile Discord in modalità dark
   ==================================== */
/* Reset base */
*, ::before, ::after {{
  box-sizing: border-box;
  border-width: 0;
  border-style: solid;
  border-color: #e5e7eb;
}}
::before, ::after {{
  --tw-content: '';
}}
html {{
  line-height: 1.5;
  -webkit-text-size-adjust: 100%;
  -moz-tab-size: 4;
  tab-size: 4;
  font-family: "Whitney", "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-feature-settings: normal;
}}
body {{
  margin: 0;
  line-height: inherit;
  background-color: #36393f;
  color: #dcddde;
  padding: 20px;
}}
/* Container principale */
.container {{
  max-width: 800px;
  margin: 0 auto;
  background-color: #2f3136;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}}
/* Header */
.header {{
  border-bottom: 1px solid #40444b;
  margin-bottom: 20px;
  padding-bottom: 10px;
}}
.header h1 {{
  color: #ffffff;
  font-size: 1.6em;
}}
.header p {{
  color: #72767d;
  font-size: 0.9em;
}}
/* Messaggi */
.message {{
  padding: 10px 0;
  border-bottom: 1px solid #40444b;
  margin-bottom: 5px;
}}
.message:last-child {{
  border-bottom: none;
}}
.message .meta {{
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}}
.message .author {{
  font-weight: 600;
  color: #ffffff;
  margin-right: 10px;
}}
.message .timestamp {{
  color: #72767d;
  font-size: 0.8em;
}}
.message .content {{
  margin-left: 40px;
  font-size: 1em;
  word-wrap: break-word;
}}
/* Embeds */
.embed {{
  background-color: #2f3136;
  border-left: 4px solid #7289da;
  padding: 10px;
  margin: 10px 0;
  border-radius: 4px;
}}
.embed .title {{
  font-size: 1em;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 5px;
}}
.embed .description {{
  font-size: 0.95em;
  color: #dcddde;
}}
.embed .fields {{
  margin-top: 10px;
}}
.embed .field {{
  margin-bottom: 10px;
}}
.embed .field .name {{
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 3px;
}}
.embed .field .value {{
  font-size: 0.9em;
  color: #dcddde;
}}
/* Avatar */
.avatar {{
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}}
.message-row {{
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}}
.message-row .message-content {{
  flex: 1;
}}
a {{
  color: #00b0f4;
  text-decoration: none;
}}
a:hover {{
  text-decoration: underline;
}}
/* Reazioni */
.reaction {{
  display: inline-flex;
  align-items: center;
  background-color: #40444b;
  color: #dcddde;
  border-radius: 12px;
  font-size: 0.8em;
  padding: 2px 6px;
  margin-right: 5px;
}}
/* Footer */
.footer {{
  border-top: 1px solid #40444b;
  margin-top: 20px;
  padding-top: 10px;
  font-size: 0.8em;
  color: #72767d;
}}
/* Pulsanti */
.button {{
  display: inline-block;
  padding: 8px 16px;
  margin: 5px 0;
  border: none;
  border-radius: 4px;
  font-size: 0.9em;
  cursor: pointer;
}}
.button.primary {{
  background-color: #7289da;
  color: #ffffff;
}}
.button.success {{
  background-color: #43b581;
  color: #ffffff;
}}
.button.danger {{
  background-color: #f04747;
  color: #ffffff;
}}
.button.secondary {{
  background-color: #747f8d;
  color: #ffffff;
}}
/* Animazioni */
@keyframes fadeIn {{
  from {{ opacity: 0; }}
  to {{ opacity: 1; }}
}}
.fade-in {{
  animation: fadeIn 0.5s ease-in-out;
}}
/* Responsive */
@media (max-width: 600px) {{
  body {{
    padding: 10px;
  }}
  .container {{
    width: 100%;
  }}
  .header h1 {{
    font-size: 1.5em;
  }}
}}
/* Altre regole per imitare Discord */
* {{
  scroll-behavior: smooth;
}}
  </style>
</head>
<body>
  <div class="container fade-in">
    <div class="header">
      <h1>Transcript del Ticket: {ticket_channel.name}</h1>
      <p>Generato automaticamente</p>
    </div>
"""
    for m in messages:
        timestamp = m.created_at.strftime("%Y-%m-%d %H:%M:%S")
        author = m.author.display_name
        content = m.content.replace("\n", "<br>") if m.content else ""
        html_content += f'<div class="message"><span class="author">{author}</span><span class="timestamp">{timestamp}</span><div class="content">{content}</div></div>\n'
        for embed_obj in m.embeds:
            embed_title = embed_obj.title if embed_obj.title else ""
            embed_desc = embed_obj.description if embed_obj.description else ""
            html_content += f'<div class="embed"><strong>{embed_title}</strong><br>{embed_desc}</div>\n'
    html_content += """
    <div class="footer">
      <p>Transcript generato il """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
    </div>
  </div>
</body>
</html>
"""
    os.makedirs("transcript", exist_ok=True)
    base_filename = f"transcript-{username}.html"
    filename = os.path.join("transcript", base_filename)
    counter = 1
    while os.path.exists(filename):
        filename = os.path.join("transcript", f"transcript-{username}({counter}).html")
        counter += 1
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    return filename

def setup(bot):
    bot.add_command(ticket)
