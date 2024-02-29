# This example requires the 'message_content' privileged intent to function.

from discord.ext import commands

import discord


class CounterBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("$"), intents=intents
        )

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")


# Bottone che quando premuto printa il proprio label per essere letto dall'input di itdschargen.py
# Può funzionare per sinput() con len(lis) <= 5, per lunghezze maggiori è necessario
# creare ulteriori righe per discord.ui.View
class Btn(discord.ui.Button):
    def __init__(self, name: str):
        super().__init__(label=name)
    async def callback(self, interaction: discord.Interaction):
        print(self.label)
        await interaction.response.edit_message(content='Selected', view=self.view)


bot = CounterBot()


# La creazione dei bottoni andrà gestita dentro a sinput()
@bot.command()
async def counter(ctx: commands.Context):
    """Starts a counter for pressing."""
    v = discord.ui.View()
    names = ['gg', 'al', 'wer']
    for n in names:
        v.add_item(Btn(n))
    await ctx.send("Press!", view=v)


from config import TOKEN

bot.run(TOKEN)
