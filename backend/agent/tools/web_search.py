from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv
load_dotenv()
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = os.getenv('TAVILY_KEY')

@tool(description='从网络搜索')
def web_search(query: str):
    tool = TavilySearch(
        max_results=5,
        topic="general",
        # include_answer=False,
        # include_raw_content=False,
        # include_images=False,
        # include_image_descriptions=False,
        # search_depth="basic",
        # time_range="day",
        # include_domains=None,
        # exclude_domains=None
    )
    res = tool.invoke({'query': query})
    return res


if __name__ == '__main__':
    res = web_search('现在的天气')
    print(res)