from typing import Literal, Optional
import discord
from discord.ext import commands
import aiohttp
from discord import app_commands
from discord.app_commands import Choice


class main_Cog(commands.Cog):
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

    def is_nsfw(interaction: discord.Interaction) -> bool:      
        if interaction.channel.is_nsfw( ) is False:
            return interaction.response.send_message("🔞 You cannot use this command outside a nsfw channel!", ephemeral=True)
        return interaction.channel.is_nsfw()

    @app_commands.command(description="NSFW neko commands!")
    @app_commands.check(is_nsfw)
    async def neko(self, interaction: discord.Interaction):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.waifu.pics/nsfw/neko") as request:
                data = await request.json()
                embed = discord.Embed(description=f"**[Image Link]({data['url']})**")
                embed.set_image(url=data['url'])       
                return await interaction.response.send_message(embed=embed)   
    
    @commands.command() 
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~"]] = None) -> None:
        if not guilds:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        assert guilds is not None
        fmt = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                fmt += 1

        await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")


    
async def setup(bot):
    await bot.add_cog(main_Cog(bot))