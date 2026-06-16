from langchain.tools  import  tool
import requests
from bs4 import BeautifulSoup
from tavily import  TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()

tavily=TavilyClient(os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query :str)-> str:
    """This tool will be searching the relible Topic in The Website and Return URL,Title,Content. """
    Response=tavily.search(query=query,max_results=5)


    output=[]
    for r in Response["results"]:
        output.append(f'Url:{r['url']}\n Title:{r['title']} \n Snippets :{r['content'][:300]}\n\n ')

    return "\n---\n".join(output)


# print(web_search.invoke("news Trending  topic AI in "))
@tool
def scrape_url(url :str) ->str:
    """Scrape and Return Clean Text Gived Url For Deep Reader or Serching ."""

    data=requests.get(url=url,headers={"User-Agent":"Mozilla/5.0"},timeout=10)
    soup=BeautifulSoup(data.text,"html.parser")

    try:
        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"NOT Fetched Url:{e}"


# print(scrape_url.invoke("https://en.wikipedia.org/wiki/Virat_Kohli"))
