import requests
from typing import Dict
from datetime import datetime

class MattermostNotifier:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def format_message(self, repo_name: str, release: Dict) -> Dict:
        """
        Formats message for Mattermost with attachments
        """
        owner, repo = repo_name.split('/')
        
        return {
            "attachments": [{
                "fallback": f"New release {release['tag_name']} in {repo_name}",
                "color": "#2E7D32",  # Зеленый цвет для новых релизов
                "pretext": f"🚀 New release in {repo_name}",
                "author_name": owner,
                "author_link": f"https://github.com/{owner}",
                "author_icon": f"https://github.com/{owner}.png",
                "title": release['name'],
                "title_link": release['html_url'],
                "text": release['body'],
                "fields": [
                    {
                        "short": True,
                        "title": "Version",
                        "value": f"`{release['tag_name']}`"
                    },
                    {
                        "short": True,
                        "title": "Released",
                        "value": datetime.fromisoformat(release['published_at']).strftime("%Y-%m-%d %H:%M UTC")
                    }
                ],
                "footer": "GitHub Release Watcher",
                "footer_icon": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
            }]
        }

    def send_notification(self, message: Dict):
        """
        Sends notification to Mattermost
        """
        if not self.webhook_url:
            return

        requests.post(self.webhook_url, json=message) 