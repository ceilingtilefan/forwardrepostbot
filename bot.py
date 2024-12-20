import discord # type: ignore
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
            forwardURL = message.reference.jump_url
            creationTime = message.message_snapshots[0].created_at
            imageExts = ["png", "jpg", "jpeg", "webp", "gif"]
            embedList = []

            if len(forwardContent) == 0:
                forwardContent = "Forward contained no text"            
            forwardEmbed = discord.Embed(title="Jump to message", url=f"{forwardURL}", description=f"{forwardContent}", timestamp=creationTime)
            forwardEmbed.set_footer(text=f"Forwarded by {author}" , icon_url=authorAvatar)
            
            await message.reply(embed=forwardEmbed, mention_author=False) 
            if forwardAttachments:
                for attachment in forwardAttachments:
                    file_ext = attachment.filename.split(".")[-1].lower()
                    if file_ext in imageExts:
                        newEmbed = discord.Embed(url='https://soggy.cat').set_image(url=str(attachment.url))
                        embedList.append(newEmbed)
                    else:
                        attachmentURLs = [attachment.url for attachment in forwardAttachments]
                        formattedURLs = "\n".join(attachmentURLs)
                try:
                    if embedList is not None:
                        await message.channel.send(embeds=embedList)
                except Exception:
                    pass
                try:
                    if attachmentURLs is not None:
                        await message.channel.send(f"Non-image attachments: {formattedURLs}")
                except Exception:
                    pass

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

with open('token.txt') as f:
    tokentxt = f.readline()
token = os.getenv('TOKEN', tokentxt)
client.run(token)
