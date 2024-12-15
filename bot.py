import discord
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user} using Discord.py version {discord.__version__}')

    async def on_message(self, message):
        if message.flags.forwarded == True:
            if len(message.message_snapshots[0].content) > 256:
                await message.channel.send("Forwarded messages must be 256 or fewer in length.", delete_after=5)
            else:
                author = message.author
                authorAvatar = message.author.avatar.url
                forwardContent = message.message_snapshots[0].content
                forwardAttachments = message.message_snapshots[0].attachments
                forwardEmbed = discord.Embed(
                    title=f"{forwardContent}",
                )
                forwardEmbed.set_footer(text=f"Forwarded by {author}", icon_url=authorAvatar)
                await message.reply(embed=forwardEmbed, mention_author=False)

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

with open('token.txt') as f:
    tokentxt = f.readline()
token = os.getenv('TOKEN', tokentxt)
client.run(token)