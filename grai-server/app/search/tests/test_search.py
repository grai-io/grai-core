from search.search import SearchClient


async def test_build():
    client = SearchClient()

    client.build()
