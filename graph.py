from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="password123")

graph.refresh_schema()

graph_schema = graph.schema
