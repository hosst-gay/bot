import aiohttp
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

class nsfw(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    async def is_nsfw(interaction: discord.Interaction) -> bool:
        if interaction.channel.is_nsfw():
            return True
        await interaction.response.send_message("🔞 You cannot use this command outside a nsfw channel!", ephemeral=True)
        return False
    
    
    @app_commands.command(description="Show NSFW neko pics! ")
    @app_commands.check(is_nsfw)
    @app_commands.choices(feature=[
        Choice(name="neko", value="neko"),
        Choice(name="waifu", value="waifu"),
        Choice(name="trap", value="trap")
    ])
    async def neko(self, interaction: discord.Interaction, feature:Choice[str]):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.waifu.pics/nsfw/{feature.name}") as request:
                print(request.url)

                data = await request.json()
                print(data['url'])
                embed = discord.Embed(description=f"**[Image Link]({data['url']})**")
                embed.set_image(url=data['url'])       
                return await interaction.response.send_message(embed=embed)   

    
    @neko.error
    async def nsfwerror(self,interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CheckFailure):
            pass

        


async def setup(bot: commands.Bot):
    await bot.add_cog(nsfw(bot))