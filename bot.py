import discord
from discord.ext import commands
from discord import Intents


intents = Intents.all()
intents.typing = False
intents.presences = False
client = commands.Bot(command_prefix = "$", intents = intents, case_insensitive=True)


@client.event
async def on_ready(): 
    print(f"Hello There")


@client.listen("on_member_update")
async def on_member_timeout(before : discord.Member, after : discord.Member):
    if after.timed_out:
        guild = after.guild
        action = discord.AuditLogAction.member_update
        entry = await get_author_from_auidt(guild, after, action)
        channel = await get_channel_from_id()

        author = entry.user
        reason = entry.reason

        title = f"{after} was muted"
        colour = discord.Colour.yellow()
        embed = await punishment_embed(author, title, colour)
        embed = await punishment_embed_contents(after, reason, embed)
        await channel.send(embed = embed)


@client.listen("on_member_remove")
async def on_member_kick(member : discord.Member):
    guild = member.guild
    action = discord.AuditLogAction.kick
    entry = await get_author_from_auidt(guild, member, action)
    channel = await get_channel_from_id()

    author = entry.user
    reason = entry.reason

    title = f"{member} was kicked"
    colour = discord.Colour.orange()
    embed = await punishment_embed(author, title, colour)
    embed = await punishment_embed_contents(author, reason, embed)
    await channel.send(embed = embed)


@client.listen("on_member_ban")
async def on_member_ban(guild : discord.Guild, user : discord.User):
    action = discord.AuditLogAction.ban
    entry = await get_author_from_auidt(guild, user, action)
    channel = await get_channel_from_id()

    author = entry.user
    reason = entry.reason    

    title = "{member} was banned"
    colour = discord.Colour.red()
    embed = await punishment_embed(author, title, colour)
    embed = await punishment_embed_contents(author, reason, embed)
    await channel.send(embed = embed)


async def punishment_embed(author : discord.Member, title : str, colour : discord.Colour) -> discord.Embed:
    embed = discord.Embed(title=title, colour=colour, timestamp=discord.utils.utcnow())
    embed.set_footer(text=f"{author}", icon_url=author.avatar)

    return embed


async def punishment_embed_contents(member : discord.Member, reason : str, embed : discord.Embed) -> discord.Embed:
    embed.set_thumbnail(url=member.avatar)

    embed.add_field(name="Mention", value=f'{member.mention}')
    embed.add_field(name="ID", value = member.id)
    embed.add_field(name="Reason", value = reason)

    return embed 


async def get_author_from_auidt(guild : discord.Guild, member : discord.Member, action : discord.AuditLogAction):  
    async for entry in guild.audit_logs(action=action):
        if entry.target == member:
            return entry


async def get_channel_from_id() -> discord.TextChannel:
    channel_id = 1234567890  #enter here the id of the channel on which you want to receive messages
    channel = client.get_channel(channel_id)
    return channel




client.run("Token")
