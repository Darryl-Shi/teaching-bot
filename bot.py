from dotenv import load_dotenv
import os
import json
import asyncio
import time
import discord
from discord.ext import commands

from main import TutorAI

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
bot.remove_command('help')

tutor_instances = {}  # dictionary to store TutorAI instances
@bot.event
async def on_ready():
    print(f'{bot.user} is connected')
    activity = discord.Activity(type=discord.ActivityType.listening, name="!help")
    await bot.change_presence(activity=activity)


@bot.command(name='learn')
async def start_conversation(ctx, *args):
    if args:
        topic = " ".join(args)
        existing_threads = ctx.channel.threads
        for thread in existing_threads:
            if thread.name == f"{ctx.author.name}'s {topic} session":
                await ctx.send(f"You already have an active session on {topic}. Please use that instead.")
        # create a new thread to start the conversation
        thread = await ctx.channel.create_thread(name=f"{ctx.author.name}'s {topic} session"); print("Thread created")
        #delete original message
        await ctx.message.delete()
        if topic not in tutor_instances:
            tutor_instances[topic] = TutorAI()
            print(tutor_instances)
        tutor = tutor_instances[topic]
        tutor.add_topic(topic)
        i = 0  # start at stage 1
        await tutor.chat(topic, i, thread) # convert stage number to string before passing to chat method
        await thread.send("Any further command can be run by responding to the first message!")
        await thread.send("To end the session, type !reset")
        await thread.send(ctx.author.mention)
        while True:
            try:
                user_input = await bot.wait_for('message', timeout=600.0, check=lambda message: message.author == ctx.author and message.channel == thread)
                if user_input.content.lower() == "next":
                    async with thread.typing():
                        i += 1
                        asyncio.create_task(tutor.chat(topic, i, thread))
                        await thread.send("To end the session, type !reset")
                elif user_input.content.lower() == "reset":
                    async with thread.typing():
                        tutor.reset(topic)
                        await thread.send("Chat reset to defaults.")
                        i = 0
                else:
                    async with thread.typing():
                        asyncio.create_task(tutor.custom_chat(topic, user_input.content, thread))
                        await thread.send("To end the session, type !reset")
            except asyncio.TimeoutError:
                await thread.send("Conversation timed out.")
                del tutor_instances[topic]  # remove the instance from the dictionary
                await thread.delete()  # delete the thread
                break
    else:
        await ctx.send("To see what I can do, please use !help")

@bot.command(name='reset')
async def reset_conversation(ctx):
    thread = ctx.channel
    topic = thread.name.split("'s ")[1].split(" session")[0]
    if topic in tutor_instances:
        tutor = tutor_instances[topic]
        tutor.reset(topic)
        await thread.send("Deleting chat and resetting to defaults...")
        await thread.delete()
        del tutor_instances[topic]  # remove the instance from the dictionary
    else:
        await thread.send("No conversation to reset.")

@bot.command(name='studybud')
async def study_bud(ctx, *args):
    if args:
        topic = " ".join(args)
        existing_threads = ctx.channel.threads
        for thread in existing_threads:
            if thread.name == f"{ctx.author.name}'s {topic} session":
                await ctx.send(f"You already have an active session on {topic}. Please use that instead.")
        # create a new thread to start the conversation
        thread = await ctx.channel.create_thread(name=f"{ctx.author.name}'s {topic} session"); print("Thread created")
        #delete original message
        await ctx.message.delete()
        if topic not in tutor_instances:
            tutor_instances[topic] = TutorAI()
            print(tutor_instances)
        tutor = tutor_instances[topic]
        await tutor.studybuddy_init(topic, thread)
        await thread.send("Study Session ready! Feel free to ask questions!")
        await thread.send("To end the session, type !reset")
        await thread.send(ctx.author.mention)
        while True:
            try:
                user_input = await bot.wait_for('message', timeout=600.0, check=lambda message: message.author == ctx.author and message.channel == thread)
                if user_input.content.lower() == "reset":
                    async with thread.typing():
                        tutor.reset(topic)
                        await thread.send("Chat reset to defaults.")
                else:
                    async with thread.typing():
                        asyncio.create_task(tutor.studybuddy_interactive(user_input.content, thread))
                        await thread.send("To end the session, type !reset")
            except asyncio.TimeoutError:
                await thread.send("Conversation timed out.")
                del tutor_instances[topic]  # remove the instance from the dictionary
                await thread.delete()  # delete the thread
                break

            

@bot.command(name='help')
async def display_help(ctx):
    help_msg = "To start a conversation with me, use the !learn or the !studybud command followed by the topic you want to learn about/study. For example: `!learn python` or `!studybud python` command. \n\nWhile in a conversation with me, you can just use regular English to ask me questions. The !learn command teaches you about the topic you ask about and the !studybud command turns the bot into a study buddy who can answer any questions you have about your work. If you want to end the conversation, type `!reset`."
    await ctx.send(help_msg)

bot.run(TOKEN)