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
            f"As characterized by saying '{target_phrase}' again, {message.author.name}'s depression level increased to {user_counters[user_id]}. 📈"
        )

    # Ensure other commands still work
    await bot.process_commands(message)

# Command to reset an individual user's counter
@bot.command(name="curedepression")
async def resetcount(ctx):
    """Allows a user to reset their own counter."""
    user_id = ctx.author.id

    if user_id in user_counters:
        user_counters[user_id] = 0 # Just in case.
        del user_counters[user_id]
        await ctx.send(f"{ctx.author.name} has been cured of depression! 🎉\nNo credits to SSRIs.")
    else:
        await ctx.send(f"Brother, you're not depressed, you can't be cured. 🤷‍♂️")

# Command to check the current count without triggering it
@bot.command(name="depressionlevel")
async def mycount(ctx):
    """Lets users check their count without saying the phrase."""
    user_id = ctx.author.id
    count = user_counters.get(user_id, 0)
    if count > 0:
        await ctx.send(f"{ctx.author.name}'s depression level is '{count}'. 📊")
    else:
        await ctx.send(f"{ctx.author.name} is not depressed. 🎉")

@bot.command(name="watchlist")
async def allcounts(ctx):
    """Displays all users' counts in the current chat, ranked from most to least."""
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

# Run the bot
token = env.token()
bot.run(token)
