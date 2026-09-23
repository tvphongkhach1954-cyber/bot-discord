import io
import discord
from discord.ext import commands

# ==============================
# TOKEN BOT
# ==============================

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise Exception("Missing DISCORD_TOKEN")


# ==============================
# INTENTS
# ==============================

intents = discord.Intents.default()
intents.message_content = True


# ==============================
# BOT
# ==============================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# ==============================
# SCRIPT
# ==============================

SCRIPTS = {

    "tsb_farm": (
        "🌾 TSB Farm",
        """
getgenv().DoServerHop = true -- change to false if you want to disable server hop on start of the script
loadstring(game:HttpGet("https://gitlab.com/zkay404-group/ProjectYielding/-/raw/main/ZKSuryuFarm"))()
"""
    ),


    "maru_farm": (
        "🌱 Maru Farm",
        """
getgenv().Key = "MARU-2PVP3-TI9IZ4-6TI-8OIAQ-UOUZF"
getgenv().id = "1173625689723895893"
loadstring(game:HttpGet("https://cdn.maruhub.online/s/mobile"))()

"""
    ),


    "banana_farm": (
        "🍌 Banana Farm",
        """
repeat wait() until game:IsLoaded() and game.Players.LocalPlayer 
getgenv().Key = "b7833189444b9029cd599c70" 
loadstring(game:HttpGet("https://raw.githubusercontent.com/obiiyeuem/vthangsitink/main/BananaHub.lua"))()

"""
    ),


    "maru_kaitun": (
        "⚡ Maru Kaitun",
        """
getgenv().Key = "MARU-2PVP3-TI9IZ4-6TI-8OIAQ-UOUZF"
getgenv().id = "1173625689723895893"
getgenv().Script_Mode = "Kaitun_Script"
loadstring(game:HttpGet("https://cdn.maruhub.online/s/mobile"))()
"""
    ),


    "banana_kaitun levi": (
        "🍌 Banana Kaitun levi",
        """
getgenv().Key = ""
getgenv().__BANANA_SCRIPT_ROUTE = "kaitun_levi"
return loadstring(game:HttpGet("https://banana-hub.xyz/loader/banana.lua"))()
"""
    )

}


# ==============================
# GỬI SCRIPT
# ==============================

async def send_script(
        interaction,
        title,
        script
):

    if len(script) <= 1900:

        await interaction.response.send_message(
            f"### {title}\n"
            f"```lua\n{script}\n```",
            ephemeral=True
        )

    else:

        file = discord.File(
            io.BytesIO(script.encode("utf-8")),
            filename=f"{title.replace(' ', '_')}.lua"
        )

        await interaction.response.send_message(
            f"### {title}\nScript dài, gửi file Lua:",
            file=file,
            ephemeral=True
        )



# ==============================
# MENU SELECT
# ==============================

class ScriptSelect(discord.ui.Select):

    def __init__(self):

        options = []

        for key, value in SCRIPTS.items():

            options.append(
                discord.SelectOption(
                    label=value[0],
                    value=key
                )
            )


        super().__init__(
            placeholder="📂 Chọn script...",
            options=options,
            custom_id="script_select"
        )


    async def callback(
            self,
            interaction
    ):

        key = self.values[0]

        title, script = SCRIPTS[key]

        await send_script(
            interaction,
            title,
            script
        )



# ==============================
# VIEW
# ==============================

class ScriptView(discord.ui.View):

    def __init__(self):

        super().__init__(
            timeout=None
        )

        self.add_item(
            ScriptSelect()
        )



# ==============================
# BOT ONLINE
# ==============================

@bot.event
async def on_ready():

    if not hasattr(bot, "view_loaded"):

        bot.add_view(
            ScriptView()
        )

        bot.view_loaded = True


    await bot.tree.sync()


    print("==========================")
    print("BOT ONLINE")
    print(bot.user)
    print("==========================")



# ==============================
# SLASH COMMAND
# ==============================

@bot.tree.command(
    name="menu",
    description="Mở menu script"
)
async def menu(
        interaction: discord.Interaction
):

    embed = discord.Embed(
        title="📂 SCRIPT MENU",
        description=
        """
Chọn script bên dưới:

🌾 TSB Farm
🌱 Maru Farm
🍌 Banana Farm
⚡ Maru Kaitun
🍌 Banana Kaitun
        """,
        color=discord.Color.green()
    )


    await interaction.response.send_message(
        embed=embed,
        view=ScriptView()
    )



@bot.tree.command(
    name="ping",
    description="Kiểm tra ping bot"
)
async def ping(
        interaction: discord.Interaction
):

    await interaction.response.send_message(
        f"🏓 Pong `{round(bot.latency*1000)}ms`"
    )



# ==============================
# PREFIX COMMAND
# ==============================

@bot.command()
async def menuprefix(ctx):
    await ctx.send(
        "📂 SCRIPT MENU",
        view=ScriptView()
    )


@bot.command()
async def pingprefix(ctx):
    await ctx.send(
        f"🏓 Pong `{round(bot.latency*1000)}ms`"
    )



# ==============================
# RUN BOT
# ==============================

bot.run(TOKEN)
