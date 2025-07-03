# Imports the libraries.
from google import genai
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import asyncio

"""Loads the .env file with the Discord token and AI api key."""
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
api_key = os.getenv("apikey")

"""This sets up the intents. Giving the bot access to only messages in the server."""
intents = discord.Intents.default()
intents.message_content = True

"""Create a bot with command prefix and intents."""
bot = commands.Bot(command_prefix='/', intents=intents)

# stores the users info.
user_chats = {}

# Keeps track of last Gemini response per user
user_responses = {} 

"""Alerts the user when the bot is ready  and sends a message on the terminal."""
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

""""This is a command that takes a random number 1 through 6 and sends it to the user, imitating a dice roll."""
@bot.command(name='dice' ,help='Rolls a die 1 through six when you say !dice')
async def send_dice(ctx):
    dice = random.randint(1,6)
    await ctx.send(f'You rolled a {dice} !')

"""This command takes the last response from Gemini, saves it to a txt file,
 and sends it through discord for the user to save."""
@bot.command(name="print", help="Prints the last prompt Gemini gave to you into a txt file.")
async def print_chat(ctx):

    user_id = ctx.author.id

    if user_id in user_responses:
        response_text = user_responses[user_id]

        filename = f"response_{user_id}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response_text)

        # Send the file to the Discord channel
        await ctx.send(file=discord.File(filename))

        # Optional: delete the file after sending
        os.remove(filename)
    else:
        await ctx.send("You haven't received a response yet.")

@bot.command(name='prompt', help='Changes the system prompt')
async def prompt(ctx, *, prompt):
    user_id = ctx.author.id

    if user_id in user_chats:
        chat = user_chats[user_id]
        def send_blocking():

            return chat.send_message(f"System: {prompt}")

        try:
            response = await asyncio.to_thread(send_blocking)
            await ctx.send("The System prompt has been changed.")
        except Exception as e:
            print(f"Gemini error: {e}")
            await ctx.send("Failed to send system prompt.")
    else:
        await ctx.send("No active chat found. Please send a message first to start a session.")
   
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
        list_dict = list(user_chats.items())
        print("User id and Gemini chat id:", user_chats)
        num_items = len(list_dict)
        print(num_items)

    chat = user_chats[user_id]
    
    """ This statment takes the response from Gemini and sends it to the user.
    It also catches any errors and alerts the user."""

    # Sets the max characters for each message.
    MAX_CHARS = 2000
    # Sends the response to the user.
    try:
        response = chat.send_message(message.content)
        text = response.text

          # Save the latest response
        user_responses[user_id] = text

        # Sends the response in chunks of 2000 characters.
        for index in range(0, len(text), MAX_CHARS):
            await message.channel.send(text[index:index+MAX_CHARS])

        # Catches any errors.
    except Exception as e: 
         print(f"Gemini error: {e}")
         await message.channel.send(" Gemini is currently overloaded.")

    await bot.process_commands(message)

# Starts the bot.
bot.run(TOKEN)