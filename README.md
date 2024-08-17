
---

# Madfut-Discord-Economy-Bot
A Madfut-focused Discord bot that manages a virtual economy system with commands for balance management, coin flips, daily bonuses, and more. Includes both admin and public commands, perfect for creating a fun and interactive environment in any Discord server centered around Madfut.

### Commands Overview

**Admin Commands:**

- **/mf_pay_all [amount] [currency]**: Pay every user in the server with the specified amount of coins, cards, or bot trades.
- **/mf_clear_all**: Clear everyone’s inventory of coins, cards, and bot trades.
- **/mf_inspect_wallet [user]**: View a specific user's wallet balance.
- **/mf_admin_pay [user] [coins] [cards] [bot_trades]**: Add coins, cards, or bot trades to a user's balance.
- **/mf_admin_remove [user] [coins] [cards] [bot_trades]**: Remove coins, cards, or bot trades from a user's balance.
- **/mf_clear_inventory**: Clear the inventory of every user in the server.
- **/mf_view_wallet [user]**: View the wallet of a specific user.
- **/reset_wallet [user]**: Reset a user's wallet to zero for all currencies.
- **/top_up_wallet [coins]**: Top up your own wallet with a specific number of coins.

**Public Commands:**

- **/ping**: Check if the bot is responsive.
- **/mf_wallet**: Check your current wallet balance of coins, cards, and bot trades.
- **/mf_withdraw_bots [amount]**: Withdraw a specific number of bot trades from your wallet.
- **/mf_withdraw_coins [amount]**: Withdraw a specific number of coins from your wallet.
- **/mf_withdraw_cards [amount]**: Withdraw a specific number of cards from your wallet.
- **/coin_flip [amount] [side] [opponent]**: Start a coin flip bet using coins.
- **/bot_flip [amount] [side] [opponent]**: Start a bot trade flip bet.
- **/card_flip [amount] [side] [opponent]**: Start a card flip bet.
- **/leaderboard**: View the top 5 users by coin balance.
- **/daily_bonus**: Claim your daily bonus of coins.
- **/gift_coins [user] [amount]**: Gift a specified amount of coins to another user.

### How to Use

**Setup**: Replace `TOKEN` with your bot token and ensure the bot has the appropriate permissions in your server.

**Run**: Start the bot and invite it to your server. Use the commands listed above to interact with the bot.

This bot is a great addition to any Discord server looking to add an interactive economy for its Madfut community members. Feel free to extend and customize the bot to suit your community’s needs!
