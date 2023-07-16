import discord
import deepl
import openai
from discord.ext import commands

auth_key = "AUTH_KEY"
translator = deepl.Translator(auth_key)
openai.api_key = "API_KEY"

def run_discord_bot():
    TOKEN = "TOKEN"
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

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == "?":
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

        await bot.process_commands(message)

    bot.run(TOKEN)

async def send_message(message, user_message, is_private):
    try:
        response = await generate_response(user_message)
        if response:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as error:
        print(error)

async def generate_response(user_message):
    # Set up your GPT-3.5 parameters
    messages = [
        {"role": "system", "content": "You are a helpful language learning assistant."},
        {"role": "user", "content": user_message}
    ]

    # Add prompts for personality
    prompts = []

    # Add prompts to the messages
    for prompt in prompts:
        messages.append({"role": "system", "content": prompt})

    # Generate a response using GPT-3.5
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=50,
        n=1,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

run_discord_bot()
