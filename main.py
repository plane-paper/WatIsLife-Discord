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
@bot.command(name="curedepression")
async def resetcount(ctx):
    """Allows a user to reset their own counter."""
    user_id = ctx.author.id

    if user_id in user_counters:
        user_counters[user_id] = 0
        await ctx.send(f"Your personal phrase count has been reset, {ctx.author.name}!")
    else:
        await ctx.send("You don't have a count yet!")

# Command to check the current count without triggering it
@bot.command(name="depressionlevel")
async def mycount(ctx):
    """Lets users check their count without saying the phrase."""
    user_id = ctx.author.id
    count = user_counters.get(user_id, 0)
    await ctx.send(f"Hey {ctx.author.name}, you've said '{target_phrase}' {count} times!")

# Run the bot
token = env.token()
bot.run(token)
