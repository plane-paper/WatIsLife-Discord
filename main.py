import discord
from discord.ext import commands

# Bot setup with necessary intents
intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix="!", intents=intents)

# Set the target phrase and count
target_phrase = "kill myself"
phrase_count = 0

# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

# Event: Listening to all messages
@bot.event
async def on_message(message):
    global phrase_count
    
    # Prevent bot from replying to itself
    if message.author == bot.user:
        return

    # Check if the message contains the target phrase
    if target_phrase in message.content.lower():
        phrase_count += 1
        await message.channel.send(f"I've heard '{target_phrase}' {phrase_count} times!")

    # Make sure other commands still work
    await bot.process_commands(message)

# Example command to reset count
@bot.command()
async def resetcount(ctx):
    global phrase_count
    phrase_count = 0
    await ctx.send("Phrase count has been reset!")

# Run the bot
bot.run("YOUR_BOT_TOKEN")
