# Import the libraries
from google import genai
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

# Load the .env file with the Discord token and AI api key
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
api_key = os.getenv("apikey")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Stores each user chat session
user_chats = {}

# Alert the user when the bot is ready on the terminal
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Roll the dice and send it to the user
@bot.command(name='dice' ,help='Rolls a die 1 through six when you say !dice')
async def send_dice(ctx):
    dice = random.randint(1,6)
    await ctx.send(f'You rolled a {dice} !')

@bot.command(name='reset' ,help='Resets the AI memory')
async def reset_memory(ctx):
    user_id = ctx.author.id
    if user_id in user_chats:
        del user_chats[user_id]
        await ctx.send("Your memory has been reset.")
    else:
        await ctx.send("You don't have an active memory to reset.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Prevent the bot from replying to itself
    
    # Ignore if the message starts with the command prefix
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    
    # Unique user ID
    user_id = message.author.id

     #  Store the message in a variable
    contents = message.content

    # Only create chat once per user
    if user_id not in user_chats:
        client = genai.Client(api_key=api_key)
        user_chats[user_id] = client.chats.create(model="gemini-2.5-flash")

    chat = user_chats[user_id]

    try:
        response = chat.send_message(message.content)
        # Sends the response to the user
        if message.content.lower():
            await message.channel.send(response.text)
    except Exception as e: 
         print(f"Gemini error: {e}")
         await message.channel.send(" Gemini is currently overloaded.")

    await bot.process_commands(message)  # IMPORTANT if you're using commands

# Start the bot
bot.run(TOKEN)