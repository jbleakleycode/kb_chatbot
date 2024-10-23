import streamlit as st
from llm import llm, embeddings
from graph import graph

from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

from langchain_core.prompts import ChatPromptTemplate


neo4jvector = Neo4jVector.from_existing_index(
    embeddings,
    graph=graph,
    index_name="ChunkVectorIndex",
    node_label="Chunk",
    text_node_property="content",
    embedding_node_property="embedding",
    retrieval_query="""
                    RETURN
                        node.content AS text,
                        score,
                        {
                            title: [(node)<-[:HAS_CHUNK]-(content:Content)<-[:HAS_CONTENT]-(article:Article) | article.name],
                            content: [(node)<-[:HAS_CHUNK]-(content:Content) | content.content],
                            sofwares: COALESCE([(node)<-[:HAS_CHUNK]-(content:Content)<-[:HAS_CONTENT]-(article:Article)-[:REFERS_TO_SOFTWARE]->(software:Software) | software.name],''),
                            operations: COALESCE([(node)<-[:HAS_CHUNK]-(content:Content)<-[:HAS_CONTENT]-(article:Article)-[:HAS_OPERATION]->(operation:Operation) | operation.name],'')
                        } AS metadata
                    """
)
    
retriever = neo4jvector.as_retriever(search_kwargs={'k': 10})
print('retriever', retriever)

instructions = (
    "Use the given context to answer the question."
    "If you don't know the answer, say you don't know."
    "Explicitly return the title of the documents/articles found and include all document names as sources in the final response."
    "If a document/article is requested, explicitly return the content (from the metadata) pertaining to the document/article."
    "If a summary of a document/article is requested, return a summary of the content (from the metadata) pertaining to the document/article."
    "If the software of a document/article is requested, return the softwares (from the metadata) pertaining to the document/article."
    "If the operation of a document/article is requested, return the operations (from the metadata) pertaining to the document/article."
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", instructions),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
plot_retriever = create_retrieval_chain(
    retriever, 
    question_answer_chain
)

def get_article_content(input):
    return plot_retriever.invoke({"input": input})
    # return neo4jvector.similarity_search_with_score(input, k=20)