import requests
from typing import List

class GitHubConnector:
    def __init__(self):
        self.data_store: List[str] = []

    def index_user_repos(self, username: str, token: str = None) -> int:
        """
        Fetches all public repos for a user.
        If token is provided, can fetch private ones too (rate limit higher).
        """
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"
        
        url = f"https://api.github.com/users/{username}/repos"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch repos: {response.status_code}")
                return 0
                
            repos = response.json()
            count = 0
            for repo in repos:
                # For this MVP, we just store the description and name.
                # A full system would clone and read files.
                desc = repo.get("description", "No description")
                name = repo.get("name")
                language = repo.get("language")
                
                knowledge_chunk = f"Repository: {name} | Language: {language} | Info: {desc}"
                self.data_store.append(knowledge_chunk)
                count += 1
            
            return count
        except Exception as e:
            print(f"Error accessing GitHub: {e}")
            return 0

    def get_knowledge(self) -> List[str]:
        return self.data_store
