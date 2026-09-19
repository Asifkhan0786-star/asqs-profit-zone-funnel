# ASQS Profit Zone Funnel V2

Ready-to-deploy Telegram funnel:

Website → Join Telegram → Telegram Bot → Membership Status

## Included
- Flask landing page
- Telegram bot with `/start`
- `/status` membership check
- Render configuration
- Environment-variable configuration
- Mobile-friendly design

## Required secrets
Never commit these values to GitHub:
- `BOT_TOKEN`
- `CHANNEL_ID`

Set them as environment variables in Render.

## Telegram setup
1. Create a bot with BotFather and copy the bot token.
2. Add the bot to your Telegram channel as an administrator.
3. Put the channel username or numeric ID in `CHANNEL_ID`.
4. Set `TELEGRAM_CHANNEL_URL` to the public invite/channel URL.

## Local run
```bash
pip install -r requirements.txt
python app.py
```

For the bot:
```bash
python bot.py
```

## Render
The included `render.yaml` defines:
- a web service for the landing page
- a worker service for the Telegram bot

Add the environment variables in the Render dashboard.

## Important
This project is designed for permission-based/community traffic. It does not scrape Telegram users, harvest private data, or send unsolicited bulk DMs.
