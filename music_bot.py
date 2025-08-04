import discord
from discord.ext import commands
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

@bot.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        return await ctx.send("❗ Join a voice channel first.")

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        vc = ctx.voice_client
        await vc.move_to(channel)
    else:
        vc = await channel.connect()

    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
            title = info.get('title', 'Unknown Title')

        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        vc.stop()
        vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts))
        await ctx.send(f"🎶 Now playing: **{title}**")
    except Exception as e:
        await ctx.send(f"⚠️ Error: {str(e)}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⛔ Disconnected.")
    else:
        await ctx.send("❌ I'm not connected.")

bot.run(os.getenv("TOKEN"))
