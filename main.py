import traceback
import keep_alive
import discord
from discord.ext import tasks
import get_token
import logging

# Logging
logging.basicConfig(filename="discord.log", level=logging.DEBUG, format= "| {asctime} | {levelname:<8} > {message}", style="{",filemode="w")

def debug(msg):
    logging.debug(msg)
def error(msg):
    logging.debug(msg)

# Token
def open_token():
    return get_token.open_token()
      
# Documentaton : https://discordpy.readthedocs.io/en/stable/search.html
BOT_USER_ID = 864559656960524359
class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        self.bot_user : discord.User = await self.fetch_user(BOT_USER_ID)
      
    async def on_message(self, msg:discord.Message):
        
        # Check messages
        msg_lower = str(msg.content).lower()
        print(f"Message from {msg.author}: {msg.content}")
        
        if msg.author.id == self.bot_user.id:
          pass
        else:
            # Message at test channel
            if msg.channel.id == 870640820364124162:
                if "https://" in msg_lower or "http://" in msg_lower:
                    await self.send_message(msg.channel.id, "Mandaram um link, ve se é skin <@!183743234084700160>")
                
                    
           
    # Use this Function with await, Ex: await send_message(id, msg) 
    async def send_message(self, channel_id, msg):
        channel = client.get_channel(channel_id)
        await channel.send(msg)

TOKEN = open_token()

client = MyClient()

client.run(TOKEN)
