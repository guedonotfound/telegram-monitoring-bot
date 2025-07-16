# Telegram Monitoring Bot

A Python-based Telegram bot that monitors specified channels for keywords and sends notifications when they are detected.

## Features

- Monitor multiple Telegram channels simultaneously
- Detect custom keywords in messages
- Send notifications to a specified Telegram chat when keywords are found
- List all accessible channels and groups with their IDs
- Easy to configure through environment variables

## Prerequisites

- Python 3.x
- Telegram API credentials (API ID and Hash)
- A Telegram Bot Token
- Access to the channels you want to monitor

## Installation

1. Clone the repository:

```bash
git clone https://github.com/guedonotfound/telegram-monitoring-bot.git
cd telegram-monitoring-bot
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:

```env
API_ID=your_api_id
API_HASH=your_api_hash
MEU_ID=your_telegram_id
CANAIS=["channel_id1", "channel_id2"]
TOKEN=your_bot_token
CHAT_ID=notification_chat_id
```

## Usage

### Main Bot

To start the monitoring bot:

```bash
python main.py
```

### List Channels

To list all accessible channels and their IDs:

```bash
python list-channels.py
```

### List Groups

To list groups and their IDs:

```bash
python list-groups.py
```

## Configuration

- `palavras_chave`: List of keywords to monitor (defined in `main.py`)
- `CANAIS`: List of channel IDs to monitor (defined in `.env`)
- `CHAT_ID`: The chat ID where notifications will be sent
- `TOKEN`: Your Telegram bot token

## Project Structure

- `main.py`: Main bot script that handles monitoring and notifications
- `list-channels.py`: Utility script to list all accessible channels
- `list-groups.py`: Utility script to list all accessible groups
- `requirements.txt`: Project dependencies

## Error Handling

The bot includes comprehensive error handling:

- Environment variable validation
- Connection error handling
- Graceful shutdown on keyboard interrupt
- Notification delivery confirmation

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## License

[Your chosen license]
