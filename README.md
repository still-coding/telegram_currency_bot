# Simple Telegram currecy converter bot

Telegram currency bot built with [grequests](https://github.com/spyoungtech/grequests) and [aiogram](https://aiogram.dev/).

### API used

Bot connects to free [CoinGecko API V3](https://www.coingecko.com/en/api/documentation), fetches exchange data and uses it co convert currency of user's choice.

### Try it out

Bot is now up and running on my private server so you can try it out here: https://t.me/goose_currency_bot.

You can do somethins like this:

![Bot usage examples](https://github.com/still-coding/telegram_currency_bot/blob/master/readme/scr.png?raw=true)

### Deploy yours

1. Obtain API token from [Telegram's BotFather](https://t.me/botfather)

2. Run containers using 
    ```shell
    docker compose up
    ```
