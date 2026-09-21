# ASQS PROFIT ZONE — Funnel V2

Website → Telegram → Bot → Membership Verification

## Render environment variables

Web:
- TELEGRAM_CHANNEL_URL
- TELEGRAM_BOT_USERNAME

Worker:
- BOT_TOKEN
- CHANNEL_ID
- TELEGRAM_CHANNEL_URL

Never commit BOT_TOKEN to GitHub.

## Telegram setup

1. Create the bot with BotFather.
2. Add the bot as an administrator to your own channel.
3. Put the channel ID in CHANNEL_ID.
4. Put the channel/invite URL in TELEGRAM_CHANNEL_URL.
5. Deploy the web service and worker from this repository.

This version is permission-based. It does not scrape private-channel members or send unsolicited bulk messages.
