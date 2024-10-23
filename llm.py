# Create the LLM
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    openai_api_key="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"
)

llm = ChatOpenAI(openai_api_key = "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", model="gpt-4-turbo")