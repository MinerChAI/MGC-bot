import asyncio
import sys

import discord
from discord.ext import commands
import clashroyale
import brawlstats

from const import *

class Sender:
    def __init__(self, ctx):
        self.ctx = ctx
        self.loop = bot.loop
        
    def write(self, s): 
        self.loop.run_until_complete(asyncio.wait([self.loop.create_task(self.ctx.send(s))]))
        sys.stdout.write(s)  
        return len(s)

bot = commands.Bot(command_prefix='$', description='Бот для MGC', command_not_found='Команды {} не существует', command_has_no_subcommands='У команды {} нет подкоманд', owner_id=426757590022881290)

cr_client = clashroyale.official_api.Client(CR_TOKEN, is_async=True)
bw_client = brawlstats.Client(BRAWL_STARS_TOKEN, is_async=True)

owners = [426757590022881290, 308628182213459989]

def isowner(author):
    if ctx.author.id in owners:
        return True
    ctx.send('У вас недостаточно лев для использования этой команды.')
    return False

@bot.group()
async def clashroyale(ctx):
    pass

@bot.group()
async def brawlstars(ctx):
    pass

@brawlstars.command(name='get-club')
async def get_club(ctx: commands.Context, tag: str):
    try:
        club = await bw_client.get_club(tag)
    except brawlstats.errors.NotFoundError:
        await ctx.send('Такого клана не существует!')
    else:
        embed = discord.Embed(title=club.name, description=club.description, color=0xffff00)
        embed.set_thumbnail(url=club.badge_url)
        embed.add_field(name='Тег', value=club.tag)
        embed.add_field(name='Статус', value=club.status)
        embed.add_field(name='Количество участников', value=club.members_count)
        embed.add_field(name='Участников онлайн', value=club.online_members)
        embed.add_field(name='Трофеи', value=club.trophies)
        embed.add_field(name='Трофеев для вступления', value=club.required_trophies)
        embed.add_field(name='ID значка, что бы это ни значило', value=club.badge_id)
    
        await ctx.send(embed=embed)

#@clashroyale.command()
#async def cards():
    #c = cr_client.get_all_cards()
    #await bot.say(c)

@bot.command()
async def info(ctx):
    await ctx.send(await bot.application_info())

@bot.command()
async def kill(ctx):
    if isowner(ctx.author):
        await bot.logout()

@bot.command(name='eval')
async def eval_(ctx, code: str):
    if isowner(ctx.author):
        global print
        print_ = print
        def print(*a, **kwa):
            if 'file' not in kwa:
                kwa['file'] = Sender(ctx)
                print_(*a, **kwa)
        try:
            await ctx.send(eval(code))
        
        
    except SyntaxError:
        exec(code)
        ctx.send('Код выполнен!')
    print = print_

@bot.event
async def on_error(event, *args, **kwargs):
    await bot.send_message(discord.Object('426757590022881290'))

bot.run(TOKEN)