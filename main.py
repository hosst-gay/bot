import os
import sqlite3
import discord
from discord.ext import commands
import asyncio
import config


class MyBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        if self.shard_count >= 1:
            print(f'Running {self.shard_count} shard')
        else:
            print(f'Running {self.shard_count} shards')
    



intents = discord.Intents.all()
bot = MyBot(command_prefix=">!", intents=intents)
bot.conn = sqlite3.connect('/var/www/hosst/website/schema/database.db')
bot.connembed = sqlite3.connect('/var/www/hosst/website/schema/embed.db')
bot.connimage = sqlite3.connect('/var/www/hosst/website/schema/image.db')
bot.conninvites = sqlite3.connect('/var/www/hosst/website/schema/invites.db')

    

async def main():
    async with bot:
        bot.wait_until_ready
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
            else:
                print(f'Unable to load {filename[:-3]}')
        await bot.load_extension('jishaku')
        await bot.start(config.token)


asyncio.run(main())

