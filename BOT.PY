import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')

# Set up the OpenAI API client
openai.api_key = OPENAI_KEY

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # Only respond to messages from other users, not from the bot itself
    if message.author == client.user:
        return
    
    if client.user in message.mentions:
        content = message.content.replace(client.user.mention,'')
        if not content.strip():
            error_message = "Say it, I dare you..."
            await message.channel.send(error_message)
            return

        # Use the OpenAI API to generate a response to the message
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{message.content}",
            max_tokens=2048,
            temperature=0.5,
        )
        # Send the response as a message in the Discord channel
        # Strip the newline character from the beginning of the response text
        response_text = response.choices[0].text.strip()
        if len(response_text) > 2000:
            # Split the response into multiple messages
            response_parts = [response_text[i:i+2000] for i in range(0, len(response_text), 2000)]
            for part in response_parts:
                await message.channel.send(part)
        else:
            await message.channel.send(response_text)

# Start the Discord bot
client.run(TOKEN)