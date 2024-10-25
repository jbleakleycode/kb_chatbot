# Create the LLM
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    openai_api_key=<Enter openAI API key here>
)

llm = ChatOpenAI(openai_api_key = <Enter openAI API key here>, model="gpt-4-turbo")
