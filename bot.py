import asyncio
import youtube_dl
import discord
import datetime
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)
deleting_messages = False
song_queue = []

@tasks.loop(seconds=1)
async def send_message(ctx):
    await ctx.channel.send("This is an auto-sent message!")

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.command()
async def auto_message_start(ctx):
    send_message.start(ctx)
    await ctx.send("Auto-send message function started.")

@bot.command()
async def auto_message_stop(ctx):
    send_message.stop()
    await ctx.send("Auto-send message function stopped.")

@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)

    confirmation_message = await ctx.send(f'Cleared {amount} messages.')
    await asyncio.sleep(2)
    await confirmation_message.delete()


@bot.command()
async def cleartoday(ctx):
    today = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    start_of_day = datetime.datetime(today.year, today.month, today.day)
    end_of_day = start_of_day + datetime.timedelta(days=1)

    await ctx.channel.purge(after=start_of_day, before=end_of_day)

    confirmation_message = await ctx.send(f"Cleared all messages from today's chat history.")
    await asyncio.sleep(2)
    await confirmation_message.delete()


@bot.command()
async def clearall(ctx):
    global delete_messages
    if ctx.author.guild_permissions.manage_messages:
        delete_messages = True
        await ctx.send("Clearing all messages. This may take some time...")

        async for message in ctx.channel.history(limit=None):
            if not delete_messages:
                await ctx.send("Message deletion stopped.")
                return
            await message.delete()

        delete_messages = False
        await ctx.send("All messages have been cleared.")
    else:
        await ctx.send("You do not have permission to use this command.")

@bot.command()
async def stopclear(ctx):
    global delete_messages
    delete_messages = False
    await ctx.send("Message deletion stopped.")

@bot.command()
async def play(ctx, *, search):
    voice_client = ctx.voice_client
    channel = ctx.author.voice.channel if ctx.author.voice else None
    
    if channel is None:
        await ctx.send("You need to be in a voice channel to play music.")
        return
    
    if voice_client is not None:
        if voice_client.channel != channel:
            await ctx.send("I'm already connected to a different voice channel.")
            return
    else:
        voice_client = await channel.connect()
        await ctx.send("I'm have connected to the voice channel.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    search_query = f'ytsearch:{search}'

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_query, download=False)
        url2play = info['entries'][0]['url']

    voice_client.play(discord.FFmpegPCMAudio(url2play))
    await ctx.send(f"I'm playing: {info['entries'][0]['title']}")

@bot.command()
async def stopplay(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def queue(ctx, *, search):
    song_queue.append(search)
    await ctx.send(f"Added '{search}' to the queue.")

@bot.command()
async def next(ctx):
    if song_queue:
        next_song = song_queue.pop(0)
        await play(ctx, search=next_song)
    else:
        await ctx.send("The queue is empty.")

@bot.command()
async def pause(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music playback paused.")
    else:
        await ctx.send("No music is currently playing or music is already paused.")

@bot.command()
async def resume(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Music playback resumed.")
    else:
        await ctx.send("No music is currently paused.")

load_dotenv()
bot.run(os.getenv("TOKEN"))
