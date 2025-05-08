import discord
from discord import Embed
import datetime
import random
import json
import os
import asyncio

from discord import FFmpegPCMAudio

FFMPEG_PATH = "ffmpeg" 

TOKEN = "" # Account token
OWNERS_FILE = "owners.json"

def load_owners():
    if os.path.exists(OWNERS_FILE):
        with open(OWNERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_owners(owners):
    with open(OWNERS_FILE, 'w') as f:
        json.dump(owners, f)

BOT_VERSION = "V1.0.0"  # Define the bot version

class SelfBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super(SelfBot, self).__init__(*args, **kwargs)
        self.owners = load_owners()
        self.boss_id = ""  # The ID of the boss user (your account ID)
        self.mocking_users = {}  

    async def on_ready(self):
        print('Logged in as {} (ID: {})'.format(self.user.name, self.user.id))
        print('------')

        activity = discord.Activity(type=discord.ActivityType.watching, name="MilanScripts Selfbot V1.0.0")
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        print('Message from {}: {}'.format(message.author, message.content))
        content = message.content.strip().lower()

        if message.author.id in self.mocking_users:
            if message.content.strip(): 
                user_name = '**{}:**'.format(self.mocking_users[message.author.id])  
                await message.channel.send('{} {}'.format(user_name, message.content))
            return

        if str(message.author.id) != self.boss_id and str(message.author.id) not in self.owners:
            return

        if content == '!time':
            now = datetime.datetime.now()
            formatted_time = now.strftime('%Y-%m-%d %H:%M:%S')
            await message.channel.send('Current time is: {}'.format(formatted_time))

        elif content == '!ping':
            latency_ms = int(self.latency * 1000)
            await message.channel.send('Pong! Latency: {} ms'.format(latency_ms))

        elif content == '!hello':
            await message.channel.send('Hello there! Hope you are having a great day! 😊')

        elif content in ('!coinflip', '!flip'):
            flip = random.choice(['Heads', 'Tails'])
            await message.channel.send('🪙 The coin landed on: **{}**!'.format(flip))

        elif content.startswith('!roll'):
            parts = content.split()
            sides = 6
            if len(parts) == 2 and parts[1]:
                sides = int(parts[1])
                if sides < 2:
                    sides = 6
            result = random.randint(1, sides)
            await message.channel.send('🎲 You rolled a {} (1-{})'.format(result, sides))

        elif content == '!joke':
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "Why did the developer go broke? Because he used up all his cache.",
                "Why do Java developers wear glasses? Because they don't see sharp.",
                "Why was the math book sad? Because it had too many problems.",
                "Why do programmers hate nature? It has too many bugs.",
                "How do you comfort a JavaScript bug? You console it.",
                "Why did the computer go to the doctor? It caught a virus.",
                "Why was the cell phone wearing glasses? It lost its contacts.",
                "Why did the programmer quit his job? Because he didn't get arrays.",
                "Why do Python programmers prefer snakes? Because they love Pythonic code!",
                "Why was the function sad? It didn’t get a return value.",
                "Why do programmers always mix up Christmas and Halloween? Because Oct 31 == Dec 25.",
                "Why did the computer keep freezing? It left its Windows open.",
                "Why was the computer cold? It left its Windows open.",
                "Why do programmers prefer using the dark web? Because they love dark mode.",
                "Why did the database administrator break up with their partner? They couldn’t find a table for two.",
                "Why do programmers prefer coffee? Because it helps them debug.",
                "Why did the programmer go broke? Because he lost his domain in a bet.",
                "Why do programmers love nature? Because it has trees (binary trees).",
                "Why did the programmer get stuck in the shower? The instructions on the shampoo bottle said: Lather, Rinse, Repeat.",
                "Why do programmers hate the outdoors? Too many bugs.",
                "Why did the programmer cross the road? To refactor the chicken’s code.",
                "Why do programmers prefer keyboards over mice? Because they don’t like point-and-click adventures."
            ]
            joke = random.choice(jokes)
            await message.channel.send('😂 {}'.format(joke))

        elif content.startswith('!mock'):
            if len(message.mentions) == 1:  
                mentioned_user = message.mentions[0]  
                if str(mentioned_user) == self.boss_id:
                    await message.channel.send("❌ You cannot mock the boss!")
                else:
                    self.mocking_users[mentioned_user.id] = mentioned_user.name 
                    await message.channel.send('🗣️ Now mocking **{}**.'.format(mentioned_user.name))
            else:
                await message.channel.send('Usage: !mock @user')

        elif content.startswith('!stopmock'):
            if len(message.mentions) == 1:  
                mentioned_user = message.mentions[0]  
                if mentioned_user.id in self.mocking_users:
                    del self.mocking_users[mentioned_user.id]
                    await message.channel.send('🛑 Stopped mocking **{}**.'.format(mentioned_user.name))
                else:
                    await message.channel.send('User **{}** is not being mocked.'.format(mentioned_user.name))
            else:
                self.mocking_users.clear()
                await message.channel.send('🛑 Stopped mocking all users.')

        elif content == '!listmocks':
            if self.mocking_users:
                mocked_users = ', '.join(['**{}**'.format(name) for name in self.mocking_users.values()])
                await message.channel.send('Currently mocking: {}'.format(mocked_users))
            else:
                await message.channel.send('No users are currently being mocked.')

        elif content == '!help':
            help_message = (
                "**SelfBot Commands**\n\n"
                "**General Commands:**\n"
                "`!time` - Get the current time\n"
                "`!ping` - Check the bot latency\n"
                "`!hello` - Get a friendly greeting\n"
                "`!coinflip` / `!flip` - Flip a coin\n"
                "`!roll [sides]` - Roll a dice (default 6 sides)\n"
                "`!joke` - Hear a programmer joke\n"
                "`!inspire` - Get an inspirational quote\n"
                "`!catfact` - Get a random cat fact\n"
                "`!dogfact` - Get a random dog fact\n"
                "`!advice` - Get a piece of advice\n"
                "`!rps` - Play Rock, Paper, Scissors with the bot\n"
                "`!fact` - Get a random fun fact\n\n"
                "**Owner Commands:**\n"
                "`!addowner [username]` - Add a new owner\n"
                "`!removeowner [username]` - Remove an owner\n"
                "`!listowners` - List all owners\n"
                "`!mock @user` - Mock a user by repeating what they say\n"
                "`!stopmock [@user]` - Stop mocking a specific user or all users\n"
                "`!listmocks` - List all users currently being mocked\n"
                "`!purge [amount]` - Purge the bot's messages\n"
                "`!remove [message_id]` - Remove a specific message by ID\n"
                "`!play` - Play an audio file in a voice channel\n"
                "`!version` - Show the bot version\n\n"
                "_Created By MilanScripts_"
            )
            await message.channel.send(help_message)

        elif content == '!version':
            if str(message.author) == self.boss_id:  
                version_message = (
                    "**Bot Version:**\n"
                    "{}\n\n"
                    "_Created By MilanScripts_"
                ).format(BOT_VERSION)
                await message.channel.send(version_message)
            else:
                await message.channel.send("❌ You do not have permission to use this command.")

        elif content.startswith('!addowner'):
            if str(message.author.id) == self.boss_id:  
                parts = content.split()
                if len(parts) == 2:
                    new_owner = parts[1]

                    if new_owner.startswith('<@') and new_owner.endswith('>'):
                        new_owner = new_owner.strip('<@!>') 

                    if new_owner not in self.owners:
                        self.owners.append(new_owner)
                        save_owners(self.owners)
                        await message.channel.send('✅ Added as an owner: <@{}> / {}'.format(new_owner, new_owner))
                    else:
                        await message.channel.send('❌ <@{}> / {} is already an owner.'.format(new_owner, new_owner))
                else:
                    await message.channel.send('Usage: `!addowner [user_id | @mention | username]`')
            else:
                await message.channel.send('❌ You do not have permission to add owners.')

        elif content.startswith('!removeowner'):
            if str(message.author.id) == self.boss_id: 
                parts = content.split()
                if len(parts) == 2:
                    owner_to_remove = parts[1]

                    if owner_to_remove.startswith('<@') and owner_to_remove.endswith('>'):
                        owner_to_remove = owner_to_remove.strip('<@!>')  

                    if owner_to_remove in self.owners:
                        self.owners.remove(owner_to_remove)
                        save_owners(self.owners)
                        await message.channel.send('✅ Removed as an owner: <@{}> / {}'.format(owner_to_remove, owner_to_remove))
                    else:
                        await message.channel.send('❌ <@{}> / {} is not an owner.'.format(owner_to_remove, owner_to_remove))
                else:
                    await message.channel.send('Usage: `!removeowner [user_id | @mention | username]`')
            else:
                await message.channel.send('❌ You do not have permission to remove owners.')

        elif content == '!listowners':
            if self.owners:
                owners_list = '\n'.join(['- <@{}> / {}'.format(owner, owner) for owner in self.owners])
                await message.channel.send('👑 **Current Owners:**\n{}'.format(owners_list))
            else:
                await message.channel.send('❌ No owners have been added yet.')

        elif content == '!inspire':
            quotes = [
                "The best way to predict the future is to invent it. - Alan Kay",
                "Life is 10% what happens to us and 90% how we react to it. - Charles R. Swindoll",
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
                "Believe you can and you're halfway there. - Theodore Roosevelt"
            ]
            quote = random.choice(quotes)
            await message.channel.send('🌟 {}'.format(quote))

        elif content == '!catfact':
            cat_facts = [
                "Cats sleep for 70% of their lives.",
                "A group of cats is called a clowder.",
                "Cats have five toes on their front paws but only four on their back paws.",
                "A cat's nose is as unique as a human fingerprint.",
                "Cats can rotate their ears 180 degrees."
            ]
            fact = random.choice(cat_facts)
            await message.channel.send('🐱 Did you know? {}'.format(fact))

        elif content == '!dogfact':
            dog_facts = [
                "Dogs have three eyelids.",
                "A dog’s sense of smell is at least 40x better than ours.",
                "Dogs can understand up to 250 words and gestures.",
                "The Basenji dog doesn’t bark—it yodels.",
                "Dogs’ noses are wet to help absorb scent chemicals."
            ]
            fact = random.choice(dog_facts)
            await message.channel.send('🐶 Did you know? {}'.format(fact))

        elif content == '!advice':
            advice_list = [
                "Don't compare yourself to others.",
                "Take breaks when you need them.",
                "Learn to say no.",
                "Stay curious and keep learning.",
                "Be kind to yourself and others."
            ]
            advice = random.choice(advice_list)
            await message.channel.send('💡 {}'.format(advice))

        elif content == '!rps':
            choices = ['Rock', 'Paper', 'Scissors']
            bot_choice = random.choice(choices)
            await message.channel.send('✊🖐✌️ I choose: **{}**!'.format(bot_choice))

        elif content == '!fact':
            facts = [
                "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
                "Octopuses have three hearts and blue blood.",
                "Bananas are berries, but strawberries are not.",
                "A day on Venus is longer than a year on Venus.",
                "Sharks existed before trees."
            ]
            fact = random.choice(facts)
            await message.channel.send('📚 Did you know? {}'.format(fact))

        elif content.startswith('!play'):
            if message.guild:  
                if message.author.voice: 
                    voice_channel = message.author.voice.channel  
                    try:
                        vc = await voice_channel.connect()

                        if not os.path.exists("sound.mp3"):
                            await message.channel.send("❌ The file `sound.mp3` does not exist.")
                            return

                        audio_source = FFmpegPCMAudio("sound.mp3", executable=FFMPEG_PATH)
                        vc.play(audio_source, after=lambda e: print("Finished playing: {}".format(e)))

                        while vc.is_playing():
                            await asyncio.sleep(1)

                        await vc.disconnect()
                        await message.channel.send("👋 Left the voice channel.")
                    except Exception as e:
                        await message.channel.send("❌ An error occurred: {}".format(e))
                else:
                    await message.channel.send("❌ You need to be in a voice channel to use this command.")
            else:
                await message.channel.send("❌ This command can only be used in a server.")

        elif content == '!listowners':
            if self.owners:
                owners_list = '\n'.join(['- <@{}> / {}'.format(owner, owner) for owner in self.owners])
                await message.channel.send('👑 **Current Owners:**\n{}'.format(owners_list))
            else:
                await message.channel.send('❌ No owners have been added yet.')

        elif content.startswith('!purge'):
            parts = content.split()
            if len(parts) == 2 and parts[1].isdigit():
                amount = int(parts[1])
                if amount > 0:
                    deleted = 0
                    async for msg in message.channel.history(limit=100): 
                        if msg.author == self.user:  
                            await msg.delete()
                            deleted += 1
                            if deleted >= amount:
                                break
                    await message.channel.send("🧹 Purged {} messages.".format(deleted))
                else:
                    await message.channel.send("❌ Please specify a positive number.")
            else:
                await message.channel.send("Usage: !purge [amount]")

        elif content.startswith('!remove'):
            parts = content.split()
            if len(parts) == 2 and parts[1].isdigit():
                message_id = int(parts[1])
                try:
                    msg_to_delete = await message.channel.fetch_message(message_id)
                    if msg_to_delete.author == self.user: 
                        await msg_to_delete.delete()
                        await message.channel.send("🗑️ Deleted message with ID {}.".format(message_id))
                    else:
                        await message.channel.send("❌ You can only delete the bot's messages.")
                except discord.NotFound:
                    await message.channel.send("❌ Message not found.")
                except discord.Forbidden:
                    await message.channel.send("❌ I don't have permission to delete that message.")
                except Exception as e:
                    await message.channel.send("❌ An error occurred: {}".format(e))
            else:
                await message.channel.send("Usage: !remove [message_id]")
if __name__ == "__main__":
    try:
        client = SelfBot()
        client.run(TOKEN, bot=False)
    except Exception as e:
        print('An error occurred: {}'.format(e))
        client = SelfBot()
        client.run(TOKEN, bot=False)
    except Exception as e:
        print('An error occurred: {}'.format(e))
