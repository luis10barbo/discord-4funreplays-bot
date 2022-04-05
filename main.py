import time
import traceback
from xmlrpc.client import Boolean
import keep_alive
import discord
from discord.ext import tasks
import get_token
import logging
import datetime
import pickle
import os
import pytz
import useful_functions

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
TRACKER_BOT_ID_TEST = 901665260560322571
TRACKER_BOT_ID_4FUN = 783428521753051136
COMMAND_PREFIX = "!!"
class MyClient(discord.Client):
    
    embed_files = {}
    embed_color = 15671657
    
    async def on_ready(self):
        print(f"Logged on as {self.user}")
        self.bot_user : discord.User = await self.fetch_user(BOT_USER_ID)
      
    async def on_message(self, message:discord.Message):
        
        # Check messages
        msg_lower = str(message.content).lower()
        print(f"Message from {message.author}: {message.content}")
        
        if message.author.id == self.bot_user.id:
          pass
          
        else:
            output = []
            output_string = ""
            
            if useful_functions.check_word_exists("luis", msg_lower):
                output.append("barbo")
            
            if useful_functions.check_word_exists("hugo", msg_lower):
                output.append("https://cdn.discordapp.com/attachments/822147876125147156/960867878855401512/hugo.gif")
            
            if useful_functions.check_word_exists("ghossert", msg_lower):
                output.append("https://cdn.discordapp.com/attachments/822147876125147156/960867878595346502/hugo2.gif")
                
            for output_entry in output:
                output_string += f"{output_entry}\n"
                
            await self.send_message(message.channel.id, output_string)
        
            # Commands
            if msg_lower.startswith(COMMAND_PREFIX):
                command_arguments = msg_lower[2:].split(" ")
                print("Command Sent, command arguments -> ", command_arguments)
                
                if command_arguments[0] == "ajuda" or command_arguments[0] == "help":
                    await self.send_help(message)
                
                # Tracker channel commands
                TRACKER_CHANNEL = 770112076986712125
                if message.channel.id == TRACKER_CHANNEL:
                    # (prefix)topdomes
                    if command_arguments[0] == "topmes":
                        await self.get_top_scores(message, 30, "month", "Mês")
                    elif command_arguments[0] == "topsemana":
                        await self.get_top_scores(message, 7, "week", "Semana")
                     
            # Message at test channel
            elif message.channel.id == 870640820364124162:
                if "https://" in msg_lower or "http://" in msg_lower:
                    await self.send_message(message.channel.id, "Mandaram um link, ve se é skin <@!183743234084700160>")      
           
    # Use this Function with await, Ex: await send_message(id, msg) 
    async def send_message(self, channel_id, msg:str = None, embed:discord.Embed = None):
        channel : discord.TextChannel = client.get_channel(channel_id)
        await channel.send(content=msg, embed=embed)


    # Functions
    async def get_top_scores(self, message:discord.Message, day_limit:int, prefix:str = "", prefix_text:str = "") -> None:
        embed_file_name = f"embeds\\{prefix}_track_{message.channel.id}"
        
        def save_embed(embed:discord.Embed) -> None:
            self.embed_files[message.channel.id] = {"created_at" : date_now,"embed_object": embed}
            with open(embed_file_name, "wb") as file:
                pickle.dump(self.embed_files[message.channel.id], file)
                
        def open_embed() -> Boolean:
            # Check if file exists and creates one
            if os.path.isfile(embed_file_name) == False:
                return 1
            
            one_day_ago_date = date_now - datetime.timedelta(days=1)
            
            # Check if exists a embed file in class for channel id
            
            with open(embed_file_name, "rb") as file:
                embed_dictionary = pickle.load(file)
                created_at_timestamp = embed_dictionary["created_at"]
                
            print(created_at_timestamp, one_day_ago_date)
                
            if created_at_timestamp > one_day_ago_date:
                return embed_dictionary["embed_object"]
            else:
                return 1
                
        async def get_bot_messages(day_limit=day_limit, message_limit=None) -> list:        
            latest_message_date = None
            one_month_ago_date = date_now - datetime.timedelta(days=day_limit)
            
            bot_messages = []
            
            # Loop through messages till date limit
            async for current_message in message.channel.history(limit=message_limit, after=one_month_ago_date):
                latest_message_date = message.created_at
                
                # If date limit has already passed, break loop
                if latest_message_date < one_month_ago_date:
                    break
                    
                # If message is from bot, append to "bot_messages" list
                if current_message.author.id == TRACKER_BOT_ID_TEST or current_message.author.id == TRACKER_BOT_ID_4FUN:
                    if len(current_message.embeds) > 0:
                        try:
                            embed : discord.Embed = current_message.embeds[0]
                            latest_message_date = current_message.created_at
                        
                            embed_title:str = embed.title
                            embed_description:str = embed.description
                            embed_author_name:str = embed.author.name

                            date:datetime.datetime = embed.timestamp
                            day = date.day
                            month = date.month
                            year = date.year
                            
                            parsed_message = {
                                "player_name" : embed_author_name.rsplit("for ", 1)[1],
                                "player_profile" : embed.author.url,
                                "map_name" : embed_title.rsplit(" [", 1)[0],
                                "map_link" : embed.url,
                                "map_difficulty" : "[" + embed_title.rsplit(" [", 1)[1],
                                "mods" : embed_description.split(" ", 1)[0],
                                "pp" : embed_description.split("\n")[3].replace("*", "").split("|")[0].replace(" pp", ""),
                                "day": day,
                                "month": month,
                                "year": year,
                                }
                            
                            bot_messages.append(parsed_message)
                        except:
                            traceback.print_exc()
                        
            # Sort by pp
            bot_messages_sorted = sorted(bot_messages, key=lambda dictionary: dictionary["pp"], reverse=True)
                    
            return bot_messages_sorted
        
        def create_embed(bot_messages:dict, play_limit:int = 15) -> discord.Embed:
            output_embed = discord.Embed()
            
            # Get output embed description
            output_description = ""
            for i in range(len(bot_messages)):
                if i == play_limit:
                    break
                    
                current_message = bot_messages[i]
                
                current_player = current_message["player_name"]
                current_player_profile = current_message["player_profile"]
                current_map = current_message["map_name"]
                current_map_link = current_message["map_link"]
                current_difficulty = current_message["map_difficulty"]
                current_mods = current_message["mods"]
                current_pp = current_message["pp"]
                current_day = current_message["day"]
                current_month = current_message["month"]
                current_year = current_message["year"]
                
                current_entry = f"\
                    **[{current_player}]({current_player_profile})\n{current_pp}pp\n\
                    [{current_map} {current_difficulty}]({current_map_link})\n\
                    +{current_mods.replace('HRHD', 'HDHR').replace('DTHD', 'HDDT').replace('FLHD', 'HDFL')}\n\
                    {current_day}/{current_month}/{current_year}\
                    **"
                output_embed.add_field(name=f"#{i + 1}", value=current_entry, inline=True)
                # output_description = "\n\n".join([output_description, f"{current_entry}"])
                
            local_timezone = pytz.timezone("Brazil/East")
            last_update_timestamp_tz = last_update_timestamp.replace(tzinfo=pytz.utc).astimezone(local_timezone) 
            
            output_embed.type = "rich"
            output_embed.url = ""
            output_embed.title = f"Top PP do {prefix_text} do canal #{message.channel.name}"
            output_embed.description = f"OBS: Essas informações só podem ser atualizadas uma vez por dia!"
            output_embed.set_footer(text=f"Última atualização: {last_update_timestamp_tz.day}/{last_update_timestamp_tz.month}/{last_update_timestamp_tz.year} às {last_update_timestamp_tz.hour}h{last_update_timestamp_tz.minute}m{last_update_timestamp_tz.second}s")
            output_embed.colour = self.embed_color
            output_embed.description = output_description
                
            return output_embed
        
        date_now = datetime.datetime.utcnow()
        
        result = open_embed()
        if result == 1:
            # Update list of pp plays
            print("Updating top PP")
            last_update_timestamp = date_now
            
            bot_messages = await get_bot_messages()

            embed = create_embed(bot_messages=bot_messages)
            save_embed(embed)
        else:
            
            embed = result
        print(result)
        await self.send_message(channel_id=message.channel.id, msg=None, embed=embed)
        
    async def send_help(self, message):
        available_commands = {
            "topmes" : "**Gerar lista de top PP do tracker feitos no mês**. A lista é atualizada a cada **24 horas.",
            "topsemana" : "**Gerar lista de top PP do tracker feitos na semana**. A lista é atualizada a cada 24 horas."
        }

        output_embed = discord.Embed()
        
        output_embed.type = "rich"
        output_embed.url = ""
        output_embed.title = f"Comandos 4fun"
        output_embed.set_footer(text=f"Bot feito por luis10barbo#3251")
        output_embed.colour = self.embed_color
        
        for i, command in zip(range(len(available_commands)), available_commands):
            command_description = available_commands[command]
            
            current_entry = command_description
            output_embed.add_field(name=f"{COMMAND_PREFIX}{command}", value=current_entry, inline=False)
            
        await self.send_message(channel_id=message.channel.id, msg=None, embed=output_embed)
            
            

TOKEN = open_token()

client = MyClient()

client.run(TOKEN)
