from algoliasearch.search_client import SearchClient


class Search:
    def generate_secured_api_key(self, parent_api_key: str, restrictions: dict = {}):
        return SearchClient.generate_secured_api_key(parent_api_key, restrictions)
