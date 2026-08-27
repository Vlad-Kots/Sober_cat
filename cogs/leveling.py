import discord
from discord.ext import commands
import json
import os
import random
import time

DATA_FILE = "data/levels.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def xp_for_level(level):
    return 5 * (level ** 2) + 50 * level + 100

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = load_data()
        self.cooldowns = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        user_id = str(message.author.id)
        now = time.time()

        if user_id in self.cooldowns and now - self.cooldowns[user_id] < 60:
            return
        self.cooldowns[user_id] = now

        if user_id not in self.data:
            self.data[user_id] = {"xp": 0, "level": 0}

        xp_gain = random.randint(15, 25)
        self.data[user_id]["xp"] += xp_gain

        current_level = self.data[user_id]["level"]
        xp_needed = xp_for_level(current_level + 1)

        if self.data[user_id]["xp"] >= xp_needed:
            self.data[user_id]["level"] += 1
            await message.channel.send(
                f"🎉 {message.author.mention} досяг рівня **{self.data[user_id]['level']}**!"
            )

        save_data(self.data)

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)

        if user_id not in self.data:
            await ctx.send(f"{member.mention} ще не має XP.")
            return

        xp = self.data[user_id]["xp"]
        level = self.data[user_id]["level"]
        xp_needed = xp_for_level(level + 1)

        embed = discord.Embed(title=f"Ранг {member.display_name}", color=discord.Color.blue())
        embed.add_field(name="Рівень", value=level, inline=True)
        embed.add_field(name="XP", value=f"{xp}/{xp_needed}", inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)

        await ctx.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        sorted_users = sorted(self.data.items(), key=lambda x: x[1]["xp"], reverse=True)[:10]

        if not sorted_users:
            await ctx.send("Ще нема даних для лідерборду.")
            return

        embed = discord.Embed(title="🏆 Топ учасників", color=discord.Color.gold())
        for i, (user_id, stats) in enumerate(sorted_users, start=1):
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f"User {user_id}"
            embed.add_field(
                name=f"{i}. {name}",
                value=f"Рівень {stats['level']} — {stats['xp']} XP",
                inline=False
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leveling(bot))