from typing import Dict, Optional
from github import Github
from github.Repository import Repository
from github.GithubException import GithubException

class GitHubClient:
    def __init__(self, token: str):
        self.github = Github(token)

    def get_latest_release(self, owner: str, repo: str) -> Optional[Dict]:
        """
        Gets the latest release for the specified repository
        """
        try:
            repo = self.github.get_repo(f"{owner}/{repo}")
            release = repo.get_latest_release()
            
            return {
                'tag_name': release.tag_name,
                'name': release.title,
                'body': release.body,
                'html_url': release.html_url,
                'published_at': release.published_at.isoformat()
            }
            
        except GithubException as e:
            print(f"Error getting latest release for {owner}/{repo}: {str(e)}")
            return None 