import discord
from discord.ext import commands
import random
import re

SPECIFIC_TRIGGERS = [
    (r"sober\s+forever", [
        "sober forever 🙌", "respect 🫡", "легенда", "based",
        "🐐 the goat", "справжній воїн", "sober forever, no cap"
    ]),
    (r"sober\s+today", [
        "я теж 💪", "one day at a time", "горжусь тобою", "so peak",
        "keep it up", "молодець сьогодні 🔥", "day 1 chad"
    ]),
    (r"(for\s+now|поки що)", [
        "sober forever, я вірю 🙏", "поки що... а там подивимось",
        "маленькими кроками 💪", "головне почати", "just for today, and that's enough"
    ]),
    (r"(not|no longer|перестав бути)\s+sober", [
        "нооо 😔", "sober city втратила громадянина",
        "well, it happens", "нічого, повертайся коли білочка пройде", "keep trying, don't give up"
    ]),
    (r"i'?m\s+sober", [
        "я теж 🙋", "sober gang 🤝", "welcome to sober city",
        "respect", "based and sober-pilled"
    ]),
]

GENERAL_RESPONSES = [
    "sober city 🏙️", "залишайся тверезим 💪", "sober? sober!",
    "хтось сказав sober?", "sober gang 🤝", "🐈‍⬛ мяу sober мяу",
    "SOBER CITY POPULATION: YOU", "based", "so peak", "no cap sober",
    "welcome to sober city, population: growing", "🙌", "🫡",
    "sober city has no exit", "one does not simply leave sober city",
    "sober o'clock", "check-in: sober ✅", "🏙️🌃 sober city nights",
    "sober city мер вітає тебе", "тримайся, sober city з тобою",
    "🐱 sober cat approves", "мур sober мур", "🍵 tea > alcohol, sober gang knows",
    "day by day 💪", "keep sober keep going", "sober squad +1",
    "🎉 sober celebration", "легенда sober city", "sober life best life",
    "тверезість це сила", "💯 sober energy", "sober vibes only",
    "🔥 sober streak continues", "не зупиняйся", "sober city вітає нового жителя",
    "🐾 sober cat walks by", "клас, so sober so real", "sober vibes detected",
    "💧 clear mind, sober city", "🌅 sober mornings hit different",
    "sober city — де кожен день перемога", "🥤 no alcohol, all vibes",
    "sober and thriving", "🧠 clear head, sober life",
    "🎯 focus mode: sober", "sober city резидент підтверджений",
    "💪 sober gains", "no sober no party (in a good way)",
    "тверезий розум — ясна ціль", "🌱 sober growth mindset",
    "sober city expanding", "🏆 sober achievement unlocked",
    "keep the sober streak alive", "🐈 sober cat nods approvingly",
    "sober is the new cool", "💫 sober energy radiating",
    "city of sober, population: us", "тримай марку, sober city чекає",
    "🎊 sober and proud", "no regrets, sober forever mindset",
    "💎 sober city diamond hands", "sober > everything else",
    "🌊 riding the sober wave", "keep calm and stay sober",
    "sober city citizens unite", "💪 tomorrow is another sober day",
    "🐱‍👤 sober cat, out here vibing", "respect the sober grind",
    "🥇 sober city gold medal energy", "sober gang never sleeps (on their goals)",
    "🌟 sober and shining", "day by day, sober city grows",
    "💥 sober power activated", "тримайся, ти на правильному шляху",
    "sober city з тобою в цьому", "🎶 sober vibes only playlist",
    "🍃 fresh air, sober mind", "sober city forever open for new residents",
    "💛 sober gang love", "keep it sober, keep it real",
    "🏔️ sober mountain climbers", "sober city has your back",
    "🌤️ clear skies, clear mind", "sober life, best decisions",
    "🐆 sober and fast (metaphorically)", "sober city архів поповнюється",
    "💪 one more sober day in the books", "🎬 sober city, main character energy",
]

class Responder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content.lower()

        if "sober" not in content and "тверез" not in content:
            return

        for pattern, responses in SPECIFIC_TRIGGERS:
            if re.search(pattern, content):
                await message.channel.send(random.choice(responses))
                return

        await message.channel.send(random.choice(GENERAL_RESPONSES))

async def setup(bot):
    await bot.add_cog(Responder(bot))