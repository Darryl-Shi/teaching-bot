import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json

from main import TutorAI

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
tutor = TutorAI()

@bot.event
async def on_ready():
    print(f'{bot.user} is connected')

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send("Hi! To start learning, use the learn command. Any further command can be run by responding to the first message! Usage: !learn <topic>")
    await bot.process_commands(message) # this line is required to enable the bot to process commands after processing the event

@bot.command(name='learn')
async def start_conversation(ctx, topic=None):
    if topic:
        tutor.topic = topic
        tutor.add_topic(tutor.topic)
        i = 0  # start at stage 1
        await tutor.chat(i, ctx)  # convert stage number to string before passing to chat method
        await ctx.send("Any further command can be run by responding to the first message!")
        while True:
            try:
                user_input = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=120.0)
                if user_input.content.lower() == "exit":
                    break
                if user_input.content.lower() == "next":
                    async with ctx.typing():
                        i += 1
                        await tutor.chat(i, ctx)
                elif user_input.content.lower() == "reset":
                    async with ctx.typing():
                        tutor.reset()
                        tutor.add_topic(tutor.topic)
                        i = 0
                        await tutor.chat(i, ctx)
                        await ctx.send("Chat has been reset to default.")
                else:
                    async with ctx.typing():
                        await tutor.custom_chat(user_input.content, ctx)  # also convert stage number to string here
            except asyncio.TimeoutError:
                await ctx.send("Conversation timed out.")
                break
    else:
        await ctx.send("Please specify a topic. Usage: !learn <topic>")

@bot.command(name='reset')
async def reset_conversation(ctx):
    tutor.reset()
    await ctx.send("Chat has been reset to default.")

@bot.command(name='commands')
async def display_help(ctx):
    help_msg = "To start a conversation with me, use the !learn command followed by the topic you want to learn about. For example: `!learn python`.\n\nWhile in a conversation with me, you can enter the following commands:\n\n`next`: move to the next stage of the conversation\n`reset`: reset the conversation to the default stage\n`exit`: end the conversation\n\nYou can also type any other message to send it to me and continue the conversation."
    await ctx.send(help_msg)

bot.run(TOKEN)
