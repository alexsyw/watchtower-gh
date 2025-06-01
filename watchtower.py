#!/usr/bin/env python3

import os
import yaml
from typing import Dict, List

from github_client import GitHubClient
from state import StateManager
from notifications import MattermostNotifier

class ReleaseWatcher:
    def __init__(self):
        self.github = GitHubClient(os.getenv('GITHUB_TOKEN'))
        self.state = StateManager(
            endpoint_url=os.getenv('R2_ENDPOINT'),
            access_key_id=os.getenv('R2_ACCESS_KEY_ID'),
            secret_access_key=os.getenv('R2_SECRET_ACCESS_KEY'),
            bucket=os.getenv('R2_BUCKET')
        )
        self.notifier = MattermostNotifier(os.getenv('MATTERMOST_WEBHOOK'))

    def check_releases(self):
        repos_to_watch_str = os.getenv('REPOS_TO_WATCH')
        if not repos_to_watch_str:
            print("REPOS_TO_WATCH environment variable is not set.")
            return

        repos_to_watch = [repo.strip() for repo in repos_to_watch_str.split(',')]

        for repo_name in repos_to_watch:
            if '/' not in repo_name:
                print(f"Invalid repository format: {repo_name}. Skipping.")
                continue

            owner, repo = repo_name.split('/')
            stored_releases = self.state.get_stored_releases(repo_name)
            
            latest_release = self.github.get_latest_release(owner, repo)
            if not latest_release:
                continue

            if latest_release['tag_name'] not in stored_releases:
                stored_releases[latest_release['tag_name']] = latest_release
                
                message = self.notifier.format_message(
                    repo_name,
                    latest_release
                )
                self.notifier.send_notification(message)
            
            self.state.store_releases(repo_name, stored_releases)

def main():
    watcher = ReleaseWatcher()
    watcher.check_releases()

if __name__ == "__main__":
    main() 