import discord
from discord.ext import commands

from django.conf import settings
from asgiref.sync import sync_to_async 

from analysis.sentiment import analyze_sentiment

# Define your bot's intents
intents = discord.Intents.default()  # Start with the default intents

# Enable the intents your bot needs
intents.messages = True  # Required to read messages
intents.message_content = True  # Required to read the message content

# Create the bot instance with the correct intents
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)  # Pass the intents to the bot

    async def on_ready(self):
        print(f'Bot {self.user} is now online!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Analyze sentiment of the message
        sentiment = analyze_sentiment(message.content)

        # Save the message and its sentiment to the database asynchronously
        await self.save_message_to_db(message, sentiment)
    
    @sync_to_async
    def save_message_to_db(self, message, sentiment):
        """Saves the Discord message and its sentiment to the database."""
        from .models import DiscordMessage
        DiscordMessage.objects.create(
            author=message.author.name,
            content=message.content,
            channel=message.channel.name,
            sentiment=sentiment,
        )

# Run the bot
def run_discord_bot():
    bot = MyBot()
    bot.run(settings.DISCORD_TOKEN)
