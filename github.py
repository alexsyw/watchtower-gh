from typing import Dict, List, Optional
from github import Github
from github.Repository import Repository
from github.GithubException import GithubException

class GitHubClient:
    def __init__(self, token: str):
        self.github = Github(token)

    def get_releases(self, owner: str, repo: str) -> List[Dict]:
        """
        Get list of releases for specified repository
        """
        try:
            repo = self.github.get_repo(f"{owner}/{repo}")
            releases = repo.get_releases()
            
            return [{
                'tag_name': release.tag_name,
                'name': release.title,
                'body': release.body,
                'html_url': release.html_url,
                'published_at': release.published_at.isoformat()
            } for release in releases]
            
        except GithubException as e:
            print(f"Error getting releases for {owner}/{repo}: {str(e)}")
            return [] 