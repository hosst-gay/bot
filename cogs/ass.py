import discord
from discord.ext import commands

class ass(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.command()
    async def users(self, ctx):

        cursor = self.bot.conn.cursor()
        cursor.execute("SELECT username FROM user")
        entries = cursor.fetchall()
        join = "\n".join(x[0] for x in entries)
        await ctx.send(join)

async def setup(bot):
    await bot.add_cog(ass(bot))