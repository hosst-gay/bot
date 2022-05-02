import discord
from discord.ext import commands
import aiohttp

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

    @commands.command()
    async def embed(self, ctx, *,username):
        cursor = self.bot.connembed.cursor()
        cursor.execute("SELECT color FROM embed WHERE username = ?", (username,))
        entries = cursor.fetchall()
        join = "\n".join(x[0] for x in entries)
        embed = discord.Embed(title=f"The color hex for user: {username}")
        embed.description = f"**{join}**"

        await ctx.send(embed=embed)


    @commands.command()
    async def geninv(self, ctx, *, username=None):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:5123/gentoken") as request:
                data = await request.json()
                await ctx.send(data['invite'])   
                
                   
               


async def setup(bot):
    await bot.add_cog(ass(bot))