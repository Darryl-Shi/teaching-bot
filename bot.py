import discord
from dotenv import load_dotenv
import os
from main import TutorAI


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())
tutor = TutorAI()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        command = message.content[1:]
        if command == 'start':
            tutor.run()
        else:
            response = tutor.custom_chat(command)
            await message.reply(response)


client.run(TOKEN)
