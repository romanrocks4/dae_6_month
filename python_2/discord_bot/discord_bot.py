# Imports the libraries.
from google import genai
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

"""Loads the .env file with the Discord token and AI api key."""
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
api_key = os.getenv("apikey")

"""This sets up the intents. Giving the bot access to only messages in the server."""
intents = discord.Intents.default()
intents.message_content = True

"""Create a bot with command prefix and intents."""
bot = commands.Bot(command_prefix='!', intents=intents)

# stores the users info.
user_chats = {}

"""Alerts the user when the bot is ready  and sends a message on the terminal."""
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

""""This is a command that takes a random number 1 through 6 and sends it to the user, imitating a dice roll."""
@bot.command(name='dice' ,help='Rolls a die 1 through six when you say !dice')
async def send_dice(ctx):
    dice = random.randint(1,6)
    await ctx.send(f'You rolled a {dice} !')

"""This command takes the id of the user that sent the command and matches it 
to a user id and chat in the saved chats. It then deletes it, reseting the bot's memory."""
@bot.command(name='reset' ,help='Resets the AI memory')
async def reset_memory(ctx):
    user_id = ctx.author.id
    if user_id in user_chats:
        del user_chats[user_id]
        await ctx.send("Your memory has been reset.")
    else:
        await ctx.send("You don't have an active memory to reset.")

"""This is the main function that takes the users message, 
gives it as a prompt to Gemini, and sends the response back."""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Prevents the bot from replying to itself.
    
    # Ignore if the message starts with the command prefix.
    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return
    
    # Gets the unique user ID.
    user_id = message.author.id

     # Stores the users message in a variable.
    contents = message.content

    """This statment checks the user_chats dictionary for the user id and 
    creates a new chat if the user is new. This is what gives the bot memory of previous prompts."""
    if user_id not in user_chats:
        client = genai.Client(api_key=api_key)
        user_chats[user_id] = client.chats.create(model="gemini-2.5-flash")
        print(user_chats)
    chat = user_chats[user_id]

    """ This statment takes the response from Gemini and sends it to the user.
    It also catches any errors and alerts the user."""
    try:
        response = chat.send_message(message.content)
        # Sends the response to the user.
        if message.content.lower():
            await message.channel.send(response.text)
    except Exception as e: 
         print(f"Gemini error: {e}")
         await message.channel.send(" Gemini is currently overloaded.")

    await bot.process_commands(message)

# Starts the bot.
bot.run(TOKEN)