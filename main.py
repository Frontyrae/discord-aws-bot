import os
import discord
import boto3
from discord.ext import commands

# ---- ENV DEĞİŞKENLERİ (Replit Secrets) ----
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
INSTANCE_ID = os.getenv("INSTANCE_ID")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")

# ---- AWS EC2 CLIENT ----
ec2 = boto3.client(
    "ec2",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)

# ---- DISCORD BOT ----
intents = discord.Intents.default()
intents.message_content = True  # Mesaj içeriğini okuyabilsin (Developer Portal'dan da açtın zaten)

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- YETKİ KONTROLÜ: Admin + Mod ----
def authorized(ctx):
    """
    Bu fonksiyon:
    - Admin (administrator)
    - Sunucuyu yönetebilen (manage_guild)
    - Mesaj yönetebilen (manage_messages)
    kişiler için True döner.
    Yani genelde admin + mod rollerine denk gelir.
    """
    perms = ctx.author.guild_permissions

    if perms.administrator:
        return True
    if perms.manage_guild:
        return True
    if perms.manage_messages:
        return True

    return False


@bot.command()
async def start(ctx):
    # Yetki kontrolü
    if not authorized(ctx):
        return await ctx.send("❌ Bu komutu sadece admin/mod kullanabilir.")

    await ctx.send("⏳ AWS Minecraft sunucusu açılıyor...")
    ec2.start_instances(InstanceIds=[INSTANCE_ID])
    await ctx.send("🟢 Sunucu başlatıldı!")


@bot.command()
async def stop(ctx):
    # Yetki kontrolü
    if not authorized(ctx):
        return await ctx.send("❌ Bu komutu sadece admin/mod kullanabilir.")

    await ctx.send("⏳ AWS Minecraft sunucusu kapatılıyor...")
    ec2.stop_instances(InstanceIds=[INSTANCE_ID])
    await ctx.send("🔴 Sunucu kapatıldı!")


bot.run(DISCORD_TOKEN)