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
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} is connected')

@bot.command(name='learn')
async def start_conversation(ctx, topic=None):
    if topic:
        # create a new thread to start the conversation
        thread = await ctx.channel.create_thread(name=f"{ctx.author.name}'s {topic} session")
        tutor.topic = topic
        #delete the original message
        await ctx.message.delete()
        tutor.add_topic(tutor.topic)
        i = 0  # start at stage 1
        await tutor.chat(i, thread) # convert stage number to string before passing to chat method
        await thread.send("Any further command can be run by responding to the first message!")
        await thread.send("To end the session, type !reset")
        await thread.send(ctx.author.mention)
        while True:
            try:
                user_input = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=120.0)
                if user_input.content.lower() == "next":
                    async with thread.typing():
                        i += 1
                        await thread.send(tutor.chat(i, thread))
                        await thread.send("To end the session, type !reset")
                elif user_input.content.lower() == "reset":
                    async with thread.typing():
                        tutor.reset()
                        tutor.add_topic(tutor.topic)
                        i = 0
                        await tutor.chat(i, thread)
                        await thread.send("Chat has been reset to default.")
                        #delete thread
                        await thread.delete()
                else:
                    async with thread.typing():
                        await tutor.custom_chat(user_input.content, thread)  # also convert stage number to string here
                        await thread.send("To end the session, type !reset")
            except asyncio.TimeoutError:
                await thread.send("Conversation timed out.")
                break
    else:
        await ctx.send("To see what I can do, please use !help")

@bot.command(name='reset')
async def reset_conversation(ctx):
    tutor.reset()
    await ctx.send("Chat has been reset to default.")

@bot.command(name='help')
async def display_help(ctx):
    help_msg = "To start a conversation with me, use the !learn command followed by the topic you want to learn about. For example: `!learn python`.\n\nWhile in a conversation with me, you can enter the following commands:\n\n`next`: move to the next stage of the conversation\n`reset`: reset the conversation to the default stage\n`exit`: end the conversation\n\nYou can also reply to any other message to send it to me and continue the conversation."
    await ctx.send(help_msg)

bot.run(TOKEN)
