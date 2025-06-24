# Import the libraries
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

# Alert the user when the bot is ready on the terminal
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Roll the dice and send it to the user
@bot.command(name='dice' ,help='Rolls a die 1 through six when you say !dice')
async def send_dice(ctx):
    dice = random.randint(1,6)
    await ctx.send(f'You rolled a {dice} !')


# Start the bot
bot.run(TOKEN)
