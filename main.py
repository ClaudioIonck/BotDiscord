import discord
import openai
from dotenv import load_dotenv
from discord.ext import commands
import os

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

intent = discord.Intents.default()
intent.members = True
bot = commands.Bot(command_prefix="!",intents=intent)

openai.api_key = OPENAI_API_KEY

# search for a message in a channel
async def search_messages_in_channel(channel, Limit=1):
    messages_list = []

    async for message in channel.history(limit=Limit, oldest_first=True):
        messages_list.append(
            {
                "role": "user" if message.author.id != bot.user.id else "system",
                "content": message.content
            }
        )
    return messages_list

def ask_gpt(messages):
    response = openai.ChatCompletion.create(
        messages=messages,
        model="gpt-3.5-turbo-16k",
        temperature=0.9,
        max_tokens=1000,
    )

    return response.choices[0].message.content

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    async with message.channel.typing():
        # Envie a mensagem para a função ask_gpt para obter uma resposta
        messages_list = await search_messages_in_channel(message.channel)
        response = ask_gpt(messages_list)

        await message.reply(response)

    await bot.process_commands(message)


bot.run(DISCORD_BOT_TOKEN)


