import os
import sqlite3
import discord
from discord.ext import commands
import asyncio
import config


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=">!", intents=intents)
conn = sqlite3.connect('/var/www/hosst/website/schema/database.db')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    

async def main():
    async with bot:
        bot.wait_until_ready
        
        await bot.load_extension('jishaku')
        await bot.start(config.token)


asyncio.run(main())

