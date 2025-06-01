import requests
from typing import Dict

class MattermostNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def format_message(self, repo_name: str, release: Dict) -> str:
        """
        Formats message for Mattermost
        """
        return f"""### 🚀 Новый релиз в {repo_name}

**Версия:** {release['tag_name']}
**Название:** {release['name']}
**Дата:** {release['published_at']}

{release['body']}

[Ссылка на релиз]({release['html_url']})"""

    def send_notification(self, message: str):
        """
        Sends notification to Mattermost
        """
        if not self.webhook_url:
            return

        payload = {
            "text": message
        }
        requests.post(self.webhook_url, json=payload) 