import discord
from discord.ext import commands
import random
import datetime

# Replace with your bot token
TOKEN = 'your-bot-token-here'

# Define the bot's intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents)

# Dictionary to store user balances
user_balances = {}
bot.coin_flip_bets = {}
last_claim_time = {}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot is ready. Logged in as {bot.user}')

def get_user_balance(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = {"coins": 0, "cards": 0, "bot_trades": 0}
    return user_balances[user_id]

@bot.tree.command(name="mf_pay_all", description="Pay every user in the server with coins, cards, or bot trades.")
@commands.has_permissions(administrator=True)
async def mf_pay_all(interaction: discord.Interaction, amount: int, currency: str):
    if currency not in ["coins", "cards", "bot_trades"]:
        await interaction.response.send_message("Invalid currency. Choose from 'coins', 'cards', or 'bot_trades'.", ephemeral=True)
        return

    guild = interaction.guild
    for member in guild.members:
        if not member.bot:
            balance = get_user_balance(member.id)
            balance[currency] += amount

    embed = discord.Embed(
        title="Mass Payment",
        description=f"Paid **{amount:,}** {currency} to every user in the server!",
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_clear_all", description="Clear everyone's inventory.")
@commands.has_permissions(administrator=True)
async def mf_clear_all(interaction: discord.Interaction):
    guild = interaction.guild
    for member in guild.members:
        if not member.bot:
            user_balances[member.id] = {"coins": 0, "cards": 0, "bot_trades": 0}

    embed = discord.Embed(
        title="Inventory Cleared",
        description="All users' inventories have been cleared.",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_inspect_wallet", description="View a specific user's wallet.")
@commands.has_permissions(administrator=True)
async def mf_inspect_wallet(interaction: discord.Interaction, user: discord.User):
    balance = get_user_balance(user.id)
    embed = discord.Embed(
        title=f"{user.name}'s Wallet",
        description=(
            f"**Coins:** {balance['coins']:,}\n"
            f"**Cards:** {balance['cards']:,}\n"
            f"**Bot Trades:** {balance['bot_trades']:,}"
        ),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Check if the bot is responsive.")
async def ping(interaction: discord.Interaction):
    embed = discord.Embed(title="Pong!", description="The bot is responsive.", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_wallet", description="Check your wallet balance.")
async def mf_wallet(interaction: discord.Interaction):
    user_id = interaction.user.id
    balance = get_user_balance(user_id)
    embed = discord.Embed(
        title="Your Wallet",
        description=(
            f"You have **{balance['coins']:,}** coins, **{balance['cards']:,}** cards, "
            f"and **{balance['bot_trades']:,}** bot trades!"
        ),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_withdraw_bots", description="Withdraw a specific number of bot trades.")
async def mf_withdraw_bots(interaction: discord.Interaction, bots: int):
    user_id = interaction.user.id
    balance = get_user_balance(user_id)

    if bots > balance["bot_trades"]:
        embed = discord.Embed(
            title="Withdrawal Error",
            description=(
                f"You attempted to withdraw **{bots:,}** bot trades, but you only have **{balance['bot_trades']:,}**."
                " Please enter a valid amount."
            ),
            color=discord.Color.red()
        )
    else:
        balance["bot_trades"] -= bots
        embed = discord.Embed(
            title="Bot Trade Withdrawal",
            description=f"{interaction.user.mention} has withdrawn **{bots:,}** bot trades.",
            color=discord.Color.green()
        )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_withdraw_coins", description="Withdraw a specific number of coins.")
async def mf_withdraw_coins(interaction: discord.Interaction, coins: int):
    user_id = interaction.user.id
    balance = get_user_balance(user_id)

    if coins > balance["coins"]:
        embed = discord.Embed(
            title="Withdrawal Error",
            description=(
                f"You attempted to withdraw **{coins:,}** coins, but you only have **{balance['coins']:,}**."
                " Please enter a valid amount."
            ),
            color=discord.Color.red()
        )
    else:
        balance["coins"] -= coins
        embed = discord.Embed(
            title="Coin Withdrawal",
            description=f"{interaction.user.mention} has withdrawn **{coins:,}** coins.",
            color=discord.Color.green()
        )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_withdraw_cards", description="Withdraw a specific number of cards.")
async def mf_withdraw_cards(interaction: discord.Interaction, cards: int):
    user_id = interaction.user.id
    balance = get_user_balance(user_id)

    if cards > balance["cards"]:
        embed = discord.Embed(
            title="Withdrawal Error",
            description=(
                f"You attempted to withdraw **{cards:,}** cards, but you only have **{balance['cards']:,}**."
                " Please enter a valid amount."
            ),
            color=discord.Color.red()
        )
    else:
        balance["cards"] -= cards
        embed = discord.Embed(
            title="Card Withdrawal",
            description=f"{interaction.user.mention} has withdrawn **{cards:,}** cards.",
            color=discord.Color.green()
        )
    await interaction.response.send_message(embed=embed)

class CoinFlipAcceptView(discord.ui.View):
    def __init__(self, initiator, currency, amount, side):
        super().__init__(timeout=60)
        self.initiator = initiator
        self.currency = currency
        self.amount = amount
        self.side = side

    @discord.ui.button(label="Accept Bet", style=discord.ButtonStyle.success)
    async def accept_bet(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.initiator:
            await interaction.response.send_message("You cannot accept your own bet!", ephemeral=True)
            return

        balance = get_user_balance(interaction.user.id)

        if balance[self.currency] < self.amount:
            await interaction.response.send_message("You don't have enough currency to accept this bet.", ephemeral=True)
            self.stop()
            return

        outcome = random.choice(["heads", "tails"])
        winner, loser = (self.initiator, interaction.user) if self.side == outcome else (interaction.user, self.initiator)

        user_balances[winner.id][self.currency] += self.amount
        user_balances[loser.id][self.currency] -= self.amount

        result_message = f"The coin landed on **{outcome.capitalize()}**!\n\n"
        result_message += f"**{winner.mention}** wins **{self.amount * 2:,}** {self.currency}!"
        await interaction.response.send_message(result_message)
        self.stop()

@bot.tree.command(name="coin_flip", description="Start a coin flip bet using coins.")
async def coin_flip(interaction: discord.Interaction, amount: int, side: str, opponent: discord.User = None):
    await execute_coin_flip(interaction, "coins", amount, side, opponent)

@bot.tree.command(name="bot_flip", description="Start a bot trade flip bet.")
async def bot_flip(interaction: discord.Interaction, amount: int, side: str, opponent: discord.User = None):
    await execute_coin_flip(interaction, "bot_trades", amount, side, opponent)

@bot.tree.command(name="card_flip", description="Start a card flip bet.")
async def card_flip(interaction: discord.Interaction, amount: int, side: str, opponent: discord.User = None):
    await execute_coin_flip(interaction, "cards", amount, side, opponent)

@bot.tree.command(name="mf_admin_pay", description="Add coins, cards, or bot trades to a user's balance.")
@commands.has_permissions(administrator=True)
async def mf_admin_pay(interaction: discord.Interaction, user: discord.User, coins: int = 0, cards: int = 0, bot_trades: int = 0):
    user_id = user.id
    balance = get_user_balance(user_id)

    balance["coins"] += coins
    balance["cards"] += cards
    balance["bot_trades"] += bot_trades

    embed = discord.Embed(
        title="Admin Pay",
        description=(
            f"Added **{coins:,}** coins, **{cards:,}** cards, "
            f"and **{bot_trades:,}** bot trades to {user.mention}'s balance."
        ),
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_admin_remove", description="Remove coins, cards, or bot trades from a user's balance.")
@commands.has_permissions(administrator=True)
async def mf_admin_remove(interaction: discord.Interaction, user: discord.User, coins: int = 0, cards: int = 0, bot_trades: int = 0):
    user_id = user.id
    balance = get_user_balance(user_id)

    balance["coins"] = max(0, balance["coins"] - coins)
    balance["cards"] = max(0, balance["cards"] - cards)
    balance["bot_trades"] = max(0, balance["bot_trades"] - bot_trades)

    embed = discord.Embed(
        title="Admin Remove",
        description=(
            f"Removed **{coins:,}** coins, **{cards:,}** cards, "
            f"and **{bot_trades:,}** bot trades from {user.mention}'s balance."
        ),
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_clear_inventory", description="Clear everyone's inventory.")
@commands.has_permissions(administrator=True)
async def mf_clear_inventory(interaction: discord.Interaction):
    guild = interaction.guild
    for member in guild.members:
        if not member.bot:
            user_balances[member.id] = {"coins": 0, "cards": 0, "bot_trades": 0}

    embed = discord.Embed(
        title="Inventory Cleared",
        description="All users' inventories have been cleared.",
        color=discord.Color.red()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="mf_view_wallet", description="View a specific user's wallet.")
@commands.has_permissions(administrator=True)
async def mf_view_wallet(interaction: discord.Interaction, user: discord.User):
    balance = get_user_balance(user.id)
    embed = discord.Embed(
        title=f"{user.name}'s Wallet",
        description=(
            f"**Coins:** {balance['coins']:,}\n"
            f"**Cards:** {balance['cards']:,}\n"
            f"**Bot Trades:** {balance['bot_trades']:,}"
        ),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="reset_wallet", description="Reset a user's wallet.")
@commands.has_permissions(administrator=True)
async def reset_wallet(interaction: discord.Interaction, user: discord.User):
    user_id = user.id
    if user_id in user_balances:
        user_balances[user_id] = {"coins": 0, "cards": 0, "bot_trades": 0}
        embed = discord.Embed(
            title="Reset Wallet",
            description=f"{user.mention}'s wallet has been reset.",
            color=discord.Color.red()
        )
    else:
        embed = discord.Embed(
            title="Reset Wallet",
            description=f"{user.mention} does not have a wallet to reset.",
            color=discord.Color.red()
        )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="top_up_wallet", description="Top up your own wallet with a specific number of coins.")
@commands.has_permissions(administrator=True)
async def top_up_wallet(interaction: discord.Interaction, coins: int):
    user_id = interaction.user.id
    balance = get_user_balance(user_id)

    balance["coins"] += coins
    embed = discord.Embed(
        title="Top Up Wallet",
        description=f"You have successfully topped up your wallet with **{coins:,}** coins.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="leaderboard", description="View the top 5 users by coin balance.")
async def leaderboard(interaction: discord.Interaction):
    leaderboard = sorted(user_balances.items(), key=lambda x: x[1]['coins'], reverse=True)

    embed = discord.Embed(title="Top 5 Users by Coin Balance", color=discord.Color.purple())

    for i, (user_id, balances) in enumerate(leaderboard[:5], start=1):
        user = bot.get_user(user_id)
        if user:
            embed.add_field(
                name=f"{i}. {user.name}",
                value=f"Coins: **{balances['coins']:,}**",
                inline=False
            )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="daily_bonus", description="Claim your daily bonus of coins.")
async def daily_bonus(interaction: discord.Interaction):
    user_id = interaction.user.id
    balance = get_user_balance(user_id)

    if user_id not in last_claim_time:
        last_claim_time[user_id] = datetime.datetime.now() - datetime.timedelta(days=1)

    current_time = datetime.datetime.now()
    time_since_last_claim = current_time - last_claim_time[user_id]

    if time_since_last_claim.total_seconds() >= 86400:
        daily_amount = 1000000
        balance["coins"] += daily_amount
        last_claim_time[user_id] = current_time
        embed = discord.Embed(
            title="Daily Bonus",
            description=f"You received **{daily_amount:,}** coins as your daily bonus!",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    else:
        time_left = datetime.timedelta(seconds=86400 - time_since_last_claim.total_seconds())
        embed = discord.Embed(
            title="Daily Bonus",
            description=f"You can claim your daily bonus in {time_left}!",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

@bot.tree.command(name="gift_coins", description="Gift coins to another user.")
async def gift_coins(interaction: discord.Interaction, recipient: discord.User, amount: int):
    user_id = interaction.user.id
    recipient_id = recipient.id
    balance = get_user_balance(user_id)
    recipient_balance = get_user_balance(recipient_id)

    if balance["coins"] < amount:
        embed = discord.Embed(
            title="Gift Error",
            description=f"You don't have enough coins to gift **{amount:,}** coins.",
            color=discord.Color.red()
        )
    else:
        balance["coins"] -= amount
        recipient_balance["coins"] += amount
        embed = discord.Embed(
            title="Gift Coins",
            description=f"You successfully gifted **{amount:,}** coins to {recipient.mention}!",
            color=discord.Color.green()
        )

    await interaction.response.send_message(embed=embed)

# Run the bot
bot.run(TOKEN)
