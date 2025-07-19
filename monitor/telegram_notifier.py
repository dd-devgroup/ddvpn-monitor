import httpx
from .config import Config


class TelegramNotifier:
    def __init__(self):
        self.token = Config.TELEGRAM_TOKEN
        self.another_token = Config.ANOTHER_TOKEN
        self.chat_id = Config.TELEGRAM_CHAT_ID
        self.thread_chat_id = Config.TELEGRAM_THREAD_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, message, parse_mode: str = "HTML"):
        if Config.TELEGRAM_LOGS:
            data = {"chat_id": self.chat_id, "text": message, "parse_mode": parse_mode}

            if self.thread_chat_id:
                data["message_thread_id"] = self.thread_chat_id

            try:
                httpx.post(self.api_url, data=data)
            except httpx.HTTPError as e:
                print(f"Failed to send message to Telegram: {e}")
        else:
            print(f"Telegram logs are disabled. Message not sent: {message}")

    # Метод pingpong проверяет доступность бота с another_token
    def pingpong(self, parse_mode: str = "HTML"):
        if not Config.TELEGRAM_LOGS:
            print("Telegram logs are disabled.")
            return

        is_alive = self.check_bot_status()
        message = "✅ Бот доступен" if is_alive else "❌ Бот недоступен"
        self.send_message(message, parse_mode=parse_mode)

    def check_bot_status(self):
        url = f"https://api.telegram.org/bot{self.another_token}/getMe"
        try:
            response = httpx.get(url, timeout=5)
            if response.status_code == 200 and response.json().get("ok"):
                return True
            return False
        except httpx.RequestError:
            return False

