import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user} using Discord.py version {discord.__version__}')

    async def on_message(self, message):
        if message.flags.forwarded == True:   
            author = message.author
            authorAvatar = message.author.avatar.url
            forwardContent = message.message_snapshots[0].content
            forwardAttachments = message.message_snapshots[0].attachments
            imageTypes = [".png", ".jpg", ".jpeg", ".webp", ".gif"]
            embedList = []

            if len(forwardContent) == 0:
                forwardContent = "Forward contained no text"            
            forwardEmbed = discord.Embed(description=f"{forwardContent}")
            forwardEmbed.set_footer(text=f"Forwarded by {author}", icon_url=authorAvatar)
            
            await message.reply(embed=forwardEmbed, mention_author=False) 
            #testing = [imageTypes for url in forwardAttachments in imageTypes]
            if forwardAttachments:
                for url in forwardAttachments:
                    newEmbed = discord.Embed(url='https://soggy.cat').set_image(url=str(url))
                    embedList.append(newEmbed)
                await message.channel.send(embeds=embedList)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

with open('token.txt') as f:
    tokentxt = f.readline()
token = os.getenv('TOKEN', tokentxt)
client.run(token)