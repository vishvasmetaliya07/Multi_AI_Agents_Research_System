from agents import search_agents,Reader_agents,writer_chain,crictic_chain
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
load_dotenv()
from rich import print


def run_multi_agents(topic : str):
    state={}

    print("now Start")
    print("-"*50)
    print(" Step 1 Serching Agents working...")
    #serching Agents step 1
    search_agent=search_agents()
    search_data=search_agent.invoke({
        "messages":[("user",f"Find Recent,Relible and detailed information About :-{topic}")]
    })

    state["search_result"]=search_data["messages"][-1].content

    print("\nNow Search_result",state["search_result"])

    # Reader Agents 
    print("Now Deep Reder Agnets")
    print("-"*50)
    print(" Step 2 Reader Agents working...")
    Reader_agent=Reader_agents()
    # Reader_agent.invoke(
    #     {
    #         "message":[("user",f"Based on this searching Result About {topic}",
    #                     f"pick up the most relevent url for this topic and deep research",
    #                     f"Here Search Resuult {state["search_result"]}")]
    #     }
    # )
    
    Reader_data=Reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"""
        Topic: {topic}

        Search Results:
        {state['search_result']}

        Choose the 3-5 most relevant URLs for the topic.
        Use the scrape_url tool to read them.
        Create a detailed research report including:

        
        - Key Findings
        - Important Facts
        - Statistics
        - Recent Developments
        - Source URLs
        """
                    )
                ]
            }
        )
    state["Reader_results"]=Reader_data["messages"][-1].content
    print("Reader")
    print("-"*50)
    print(" Step 1 Serching Agents working...")
    print(state["Reader_results"])

    report_combine=({
        "search_result":state["search_result"],
        "Reader_result":state["Reader_results"]
    })
    state["report"]=writer_chain.invoke({
        "topic":topic,
        "report":report_combine
    })
    state["critic"]=crictic_chain.invoke({
        "topic":topic,
        "report":state["report"]
    })

    print("Report is the ")
    print("**"*50)
    print(state["report"])
    print("**"*50)

    print("Report is the ")
    print("**"*50)
    print(state["critic"])
    print("**"*50)
    return state



if __name__ =="__main__":
    user=input("Enter topic you want deep research :")
    run_multi_agents(user)
