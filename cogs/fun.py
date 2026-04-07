""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import random

import aiohttp
import discord
import math
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime

class Choice(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Heads", style=discord.ButtonStyle.blurple)
    async def confirm(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "heads"
        self.stop()

    @discord.ui.button(label="Tails", style=discord.ButtonStyle.blurple)
    async def cancel(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "tails"
        self.stop()


class RockPaperScissors(discord.ui.Select):
    def __init__(self) -> None:
        options = [
            discord.SelectOption(
                label="Scissors", description="You choose scissors.", emoji="✂"
            ),
            discord.SelectOption(
                label="Rock", description="You choose rock.", emoji="🪨"
            ),
            discord.SelectOption(
                label="Paper", description="You choose paper.", emoji="🧻"
            ),
        ]
        super().__init__(
            placeholder="Choose...",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        choices = {
            "rock": 0,
            "paper": 1,
            "scissors": 2,
        }
        user_choice = self.values[0].lower()
        user_choice_index = choices[user_choice]

        bot_choice = random.choice(list(choices.keys()))
        bot_choice_index = choices[bot_choice]

        result_embed = discord.Embed(color=0xBEBEFE)
        result_embed.set_author(
            name=interaction.user.name, icon_url=interaction.user.display_avatar.url
        )

        winner = (3 + user_choice_index - bot_choice_index) % 3
        if winner == 0:
            result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xF59E42
        elif winner == 1:
            result_embed.description = f"**You won!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0x57F287
        else:
            result_embed.description = f"**You lost!**\nYou've chosen {user_choice} and I've chosen {bot_choice}."
            result_embed.colour = 0xE02B2B

        await interaction.response.edit_message(
            embed=result_embed, content=None, view=None
        )


class RockPaperScissorsView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.add_item(RockPaperScissors())


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="randomfact", description="Get a random fact.")
    async def randomfact(self, context: Context) -> None:
        """
        Get a random fact.

        :param context: The hybrid command context.
        """
        # This will prevent your bot from stopping everything when doing a web request - see: https://discordpy.readthedocs.io/en/stable/faq.html#how-do-i-make-a-web-request
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://uselessfacts.jsph.pl/random.json?language=en"
            ) as request:
                if request.status == 200:
                    data = await request.json()
                    embed = discord.Embed(description=data["text"], color=0xD75BF4)
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API, please try again later",
                        color=0xE02B2B,
                    )
                await context.send(embed=embed)

    @commands.hybrid_command(
        name="coinflip", description="Make a coin flip, but give your bet before."
    )
    async def coinflip(self, context: Context) -> None:
        """
        Make a coin flip, but give your bet before.

        :param context: The hybrid command context.
        """
        buttons = Choice()
        embed = discord.Embed(description="What is your bet?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.
        result = random.choice(["heads", "tails"])
        if buttons.value == result:
            embed = discord.Embed(
                description=f"Correct! You guessed `{buttons.value}` and I flipped the coin to `{result}`.",
                color=0xBEBEFE,
            )
        else:
            embed = discord.Embed(
                description=f"Woops! You guessed `{buttons.value}` and I flipped the coin to `{result}`, better luck next time!",
                color=0xE02B2B,
            )
        await message.edit(embed=embed, view=None, content=None)

    @commands.hybrid_command(
        name="rps", description="Play the rock paper scissors game against the bot."
    )
    async def rock_paper_scissors(self, context: Context) -> None:
        """
        Play the rock paper scissors game against the bot.

        :param context: The hybrid command context.
        """
        view = RockPaperScissorsView()
        await context.send("Please make your choice", view=view)

    @commands.hybrid_command(name="age", description="calculates the age")
    async def age(self, context: Context, birthdate: str) -> None:
        birthdate = datetime.strptime(birthdate, "%d-%m-%Y")
        today = datetime.today()
        age = ((today - birthdate).days / 365)
        await context.send(f"You are {int(age)} years old!")

    @commands.hybrid_command(name="centimeters", description="converts inches to centimeters")
    async def centimeters(self, context: Context, inches: float):
        centimeters = (inches * 2.54)
        await context.send(f"that is {float(centimeters)} centimeters")

    @commands.hybrid_command(name='temperature', description="Converts degree fahrenheit to degree celsius.")
    async def temperature(self, context: Context, fahrenheit: float) -> None:
        celsius = (fahrenheit - 32) * 5 / 9
        await context.send(f'{fahrenheit} degree F is {celsius} degree celsius.')

    @commands.hybrid_command(name='calculator', description="Calculates the answer to the expression.")
    async def calculator(self, context: Context, num: str) -> None:
        formatted_string = num.replace(' ', '')
        sum1 = eval(formatted_string)
        rounded_num = math.ceil(sum1)
        await context.send(f"The final answer for the expression is: {int(rounded_num)}!")

    def caesar_cipher(self, message: str, shift: int, decrypt: bool):
        # if decrypt == False, the function is used for encryption
        # if decrypt == True, the function is used for decryption
        if decrypt == True:
            shift = -shift
        return ''.join(chr((ord(char) - 97 + shift) % 26 + 97) if char.isalpha() else char for char in
                       message.lower())

    @commands.hybrid_command(name='encrypt', description="Calculates the answer to the expression.")
    async def encrypt(self, context: Context, message: str, shift: int) -> None:
        encrypt = self.caesar_cipher(message, shift, decrypt=False)
        await context.send(f"The encrypted code is {encrypt}!")

    @commands.hybrid_command(name='decrypt', description="Calculates the answer to the expression.")
    async def decrypt(self, context: Context, message: str, shift: int) -> None:
        decrypt = self.caesar_cipher(message, shift, decrypt=True)
        await context.send(f"The original was {decrypt}!")


async def setup(bot) -> None:
    await bot.add_cog(Fun(bot))
