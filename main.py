import discord
from discord.ext import commands
import json
import env
import logging
import traceback
from datetime import datetime

# Setup bot with necessary intents
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration
target_phrase = "kill myself"
counter_file = "user_counters.json"
user_counters = {}  # Dictionary to track counts per user

# Setup logging
logging.basicConfig(
    filename=f"bot_error_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Load counter
def load_counters():
    global user_counters
    try:
        with open(counter_file, "r") as file:
            user_counters = json.load(file)
        print("User counters loaded successfully.")
    except FileNotFoundError:
        print("No previous counter file found, starting fresh.")
        user_counters = {}
    except Exception as e:
        print(f"Failed to load counters: {e}")
        logging.error(f"Failed to load counters: {e}\n{traceback.format_exc()}")

# Save counter
def save_counters():
    try:
        with open(counter_file, "w") as file:
            json.dump(user_counters, file, indent=4)
        print("User counters saved.")
    except Exception as e:
        print(f"Failed to save counters: {e}")
        logging.error(f"Failed to save counters: {e}\n{traceback.format_exc()}")

# Event: Bot is ready
@bot.event
async def on_ready():
    load_counters()
    print(f"Bot is online as {bot.user}")

# Event: Catch ALL unhandled errors globally
@bot.event
async def on_error(event, *args, **kwargs):
    error_message = f"Unhandled exception in event: {event}\n{traceback.format_exc()}"
    print(error_message)  # Print error to console
    logging.error(error_message)  # Log error to file

# Event: Listening to all messages
@bot.event
async def on_message(message):
    try:
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
            save_counters()

            # Respond with the personalized count
            await message.channel.send(
                f"As characterized by saying '{target_phrase}' again, {message.author.name}'s depression level increased to {user_counters[user_id]}. 📈"
            )

        # Ensure other commands still work
        await bot.process_commands(message)
    except Exception as e:
        error_message = f"Error processing message from {message.author}: {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        await message.channel.send("Oops, something went wrong! 😓")

# Command to reset an individual user's counter
@bot.command(name="curedepression")
async def resetcount(ctx):
    try:
        user_id = ctx.author.id

        if user_id in user_counters:
            user_counters[user_id] = 0 # Just in case.
            del user_counters[user_id]
            save_counters()
            await ctx.send(f"{ctx.author.name} has been cured of depression! 🎉\nNo credits to SSRIs.")
        else:
            await ctx.send(f"Brother, you're not depressed, you can't be cured. 🤷‍♂️")
    except Exception as e:
        error_message = f"Error in resetcount command: {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        await ctx.send("Oops, something went wrong while resetting your count! 😓")

# Command to check the current count without triggering it
@bot.command(name="depressionlevel")
async def mycount(ctx):
    try:
        user_id = ctx.author.id
        count = user_counters.get(user_id, 0)
        if count > 0:
            await ctx.send(f"{ctx.author.name}'s depression level is '{count}'. 📊")
        else:
            await ctx.send(f"{ctx.author.name} is not depressed. 🎉")
    except Exception as e:
        error_message = f"Error in mycount command: {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        await ctx.send("Oops, something went wrong while checking your count! 😓")

@bot.command(name="watchlist")
async def allcounts(ctx):
    try:
        active_counts = {uid: count for uid, count in user_counters.items() if count > 0}

        if not active_counts:
            await ctx.send("Nobody is depressed. 🎉")
            return

        # Sort users by count (highest to lowest)
        sorted_counts = sorted(active_counts.items(), key=lambda x: x[1], reverse=True)

        # Build the leaderboard
        counts_list = []
        for rank, (user_id, count) in enumerate(sorted_counts, start=1):
            user = await bot.fetch_user(user_id)
            counts_list.append(f"**#{rank} {user.name}**: level {count}")

        # Send the list as a nicely formatted message
        counts_message = "\n".join(counts_list)
        await ctx.send(f"🏅 **Suicide Likelihood Level:**\n{counts_message}")
    except Exception as e:
        error_message = f"Error in allcounts command: {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.error(error_message)
        await ctx.send("Oops, something went wrong while fetching the leaderboard!")

@bot.event
async def on_command_error(ctx, error):
    error_message = f"Command error: {error}\n{traceback.format_exc()}"
    print(error_message)
    logging.error(error_message)
    await ctx.send("Oops, something went wrong with the command! 🤖")

# Run the bot
token = env.token()
bot.run(token)
