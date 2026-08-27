import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Учасника кікнуто",
            description=f"{member.mention} був кікнутий.\nПричина: {reason or 'не вказана'}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="Учасника забанено",
            description=f"{member.mention} був забанений.\nПричина: {reason or 'не вказана'}",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 5):
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"Видалено {len(deleted) - 1} повідомлень.")
        await msg.delete(delay=3)

    @kick.error
    @ban.error
    async def permission_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У тебе немає прав для цієї команди.")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("Не можу знайти такого учасника.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
    