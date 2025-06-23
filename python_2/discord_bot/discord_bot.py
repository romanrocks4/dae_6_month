import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

# Load the .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='quote' ,help='Responds with a random quote from Brooklyn 99')
async def send_quote(ctx):
    quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        'Cool cool cool, no doubt no doubt.'
    ]
    await ctx.send(random.choice(quotes))


# Start the bot
bot.run(TOKEN)
