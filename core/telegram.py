import html
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_message(text: str) -> bool:
    """
    Sends a message to the Telegram Bot API sendMessage endpoint with a 5-second timeout.
    Escapes HTML. Never raises an exception: on failure logs and returns False.
    """
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')

    if not token or not chat_id:
        logger.warning("Telegram bot token or chat ID is not configured.")
        return False

    escaped_text = html.escape(str(text))
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': str(chat_id),
        'text': escaped_text,
        'parse_mode': 'HTML',
    }

    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        if not data.get('ok'):
            logger.error("Telegram API returned not ok: %s", data)
            return False
        return True
    except Exception as exc:
        logger.error("Failed to send Telegram message: %s", exc)
        return False
