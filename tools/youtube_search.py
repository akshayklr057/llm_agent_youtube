import os
from typing import Any, Optional

import requests
from smolagents.tools import Tool


class YouTubeAPITool(Tool):
    name = "youtube_search"
    description = "Uses YouTube Search API to search videos on YouTube based on your query (think a YouTube search) then returns the top search results."
    inputs = {'query': {'type': 'string', 'description': 'The search query to perform.'}}
    output_type = "string"

    def __init__(self, max_results=10, **kwargs):
        super().__init__()
        self.max_results = max_results
        self.search_api = "https://www.googleapis.com/youtube/v3/search"
        try:
            from duckduckgo_search import DDGS
        except ImportError as e:
            raise ImportError(
                "You must install package `duckduckgo_search` to run this tool: for instance run `pip install duckduckgo-search`."
            ) from e
        self.ddgs = DDGS(**kwargs)

    def forward(self, query: str) -> str:
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": self.max_results,
            "key": os.getenv("YOUTUBE_API_KEY"),
        }
        response = requests.get(self.search_api, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data["items"]:
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                print(f"Title: {title}")
                print(f"URL: https://www.youtube.com/watch?v={video_id}\n")
            postprocessed_results =  [
                f"Title: {item['snippet']['title']} | URL: https://www.youtube.com/watch?v={item['id']['videoId']}"
                for item in data["items"]
            ]
            return postprocessed_results
        else:
            raise Exception("Error:", response.json())