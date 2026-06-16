from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 
from langchain_mistralai.chat_models import ChatMistralAI
import os 
from dotenv import load_dotenv
from tools import web_search,scrape_url
load_dotenv()


llm=ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.2
    )


def search_agents():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

def Reader_agents():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


from langchain_core.prompts import ChatPromptTemplate

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert research writer.

Your task:
1. Analyze the provided research report.
2. Improve accuracy, clarity, completeness, and structure.
3. Remove duplicate or unreliable information.
4. Present information in a professional and easy-to-read format.
5. Use only information supported by the provided report.
6. Preserve all source URLs mentioned in the report.
7. Write in a neutral, factual, and well-researched style.

Requirements:
- Clear introduction
- Minimum 3 key findings/features
- Detailed explanations
- Recent and relevant insights if available in the report
- Strong conclusion
- Sources section containing all URLs found in the report

Output must be valid Markdown.
"""
    ),
    (
        "human",
        """
Research Topic:
{topic}

Research Report:
{report}

Generate a comprehensive research article using the following format:

# {topic}

## Introduction
Provide a concise overview of the topic.

## Key Findings
- Finding 1
- Finding 2
- Finding 3
(Add more if relevant.)

## Detailed Analysis
Explain the findings with supporting details.

## Conclusion
Summarize the most important insights.

## Sources
List all source URLs mentioned in the report.
"""
    )
])
writer_chain=writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a research quality evaluator.

Evaluate the report on:
- Accuracy
- Completeness
- Clarity
- Source Quality
- Structure

Give a score from 1-10 for each category and an overall score.

Provide:
1. Strengths
2. Weaknesses
3. Missing Information
4. Improvement Suggestions

Be concise and objective.
"""
    ),
    (
        "human",
        """
Topic:
{topic}

Research Report:
{report}
"""
    )
])
crictic_chain=critic_prompt | llm  | StrOutputParser()
