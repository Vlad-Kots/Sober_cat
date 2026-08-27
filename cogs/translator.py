import discord
from discord.ext import commands
from discord import app_commands
from deep_translator import GoogleTranslator
import json
import os

DATA_FILE = "data/user_languages.json"

LANGUAGES = {
    "uk": "Українська",
    "en": "English",
    "pl": "Polski",
    "de": "Deutsch",
    "fr": "Français",
    "es": "Español",
    "ja": "日本語",
}

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class LanguageSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label=name, value=code)
            for code, name in LANGUAGES.items()
        ]
        super().__init__(
            placeholder="Обери свої мови (можна кілька)",
            min_values=1,
            max_values=len(options),
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        data = load_data()
        user_id = str(interaction.user.id)
        data[user_id] = self.values
        save_data(data)

        selected_names = [LANGUAGES[code] for code in self.values]
        await interaction.response.send_message(
            f"Твої мови збережено: {', '.join(selected_names)}",
            ephemeral=True
        )


class LanguageSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(LanguageSelect())


class TranslationView(discord.ui.View):
    def __init__(self, translations: dict):
        super().__init__(timeout=300)
        self.translations = translations
        self.expanded = False

    def render(self, full=False):
        items = list(self.translations.items())
        if not full:
            items = items[:1]

        lines = []
        for code, text in items:
            lines.append(f"**{LANGUAGES.get(code, code)}:** {text}")
        return "\n".join(lines)

    @discord.ui.button(label="Показати ще переклади ▾", style=discord.ButtonStyle.secondary)
    async def toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.expanded = not self.expanded
        button.label = "Згорнути ▴" if self.expanded else "Показати ще переклади ▾"
        content = self.render(full=self.expanded)
        await interaction.response.edit_message(content=content, view=self)


class Translator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Перекласти",
            callback=self.translate_context,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @app_commands.command(name="setlang", description="Обери мови для перекладу")
    async def setlang(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "Обери свої мови:",
            view=LanguageSelectView(),
            ephemeral=True
        )

    async def translate_context(self, interaction: discord.Interaction, message: discord.Message):
        if not message.content:
            await interaction.response.send_message("Нема тексту для перекладу.", ephemeral=True)
            return

        data = load_data()
        user_id = str(interaction.user.id)
        user_langs = data.get(user_id, ["en"])

        translations = {}
        for lang in user_langs:
            try:
                translated = GoogleTranslator(source="auto", target=lang).translate(message.content)
                translations[lang] = translated
            except Exception:
                continue

        if not translations:
            await interaction.response.send_message("Не вдалось перекласти.", ephemeral=True)
            return

        view = TranslationView(translations)
        content = view.render(full=False)

        if len(translations) > 1:
            await interaction.response.send_message(content, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(content, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Translator(bot))