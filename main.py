import discord
from discord.ext import commands
import env

# Setup bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
target_phrase = "kill myself"
user_counters = {}  # Dictionary to track counts per user

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Event: Listening to all messages
@bot.event
async def on_message(message):
    # Prevent bot from replying to itself
    if message.author == bot.user:
        return

    # User-specific counting
    user_id = message.author.id

    # If the message contains the target phrase
    if target_phrase in message.content.lower():
        if user_id not in user_counters:
            user_counters[user_id] = 0
        user_counters[user_id] += 1

        # Respond with the personalized count
        await message.channel.send(
            f"Hey {message.author.name}, I've heard '{target_phrase}' from you {user_counters[user_id]} times!"
        )

    # Ensure other commands still work
    await bot.process_commands(message)

# Command to reset an individual user's counter
@bot.command()
async def resetcount(ctx):
    user_id = ctx.author.id
    user_counters[user_id] = 0
    await ctx.send(f"Your personal phrase count has been reset!")

# Run the bot
token = env.token()
bot.run(token)
