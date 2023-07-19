import discord
import deepl
from music_links import music_tracks
from discord.ext import commands
import random
from latex import build_pdf
from sympy import sympify
import os

auth_key = "DEEPL_TOKEN"
translator = deepl.Translator(auth_key)

def run_discord_bot():
    TOKEN = "DISCORD_TOKEN"
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.command()
    async def japanese(ctx, *, text):
        translation = translator.translate_text(text, target_lang='JA')
        await ctx.send(translation)

    @bot.command()
    async def english(ctx, *, text):
        translation = translator.translate_text(text, target_lang='EN-GB')
        await ctx.send(translation)

    @bot.command()
    async def jukebox(ctx):
        song_name, song_link = random.choice(list(music_tracks.items()))
        await ctx.send(f"Now playing {song_name} \n" + song_link)

    @bot.command()
    async def latex(ctx, *, equation):
        try:
            expression = sympify(equation)
            result = expression.evalf()
            pdf = build_pdf(equation)
            pdf.save_to("/path/to/temp.pdf")
            await ctx.send(f"Result: {result}")
            await ctx.send(file=discord.File("/path/to/temp.pdf"))
            os.remove("/path/to/temp.pdf")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")


    bot.run(TOKEN)


run_discord_bot()
