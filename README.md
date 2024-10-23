Created by Jacob Bleakley

This repository does not explain how the KB is created. That is found at 
ingestion: https://github.com/jacobbleakley-neo4j/ingestion
transformation: https://github.com/jacobbleakley-neo4j/neo4j-kb-db-creation

Currently the database has been downloaded into 'neo4j.dump'. This can be used to spin up the db with ontologies and content from 'EMEA Services' Google Drive folder in a Neo4j database.

The 'bot.py' is the main script that pulls in functions from the other python files. The application is streamlined due to the use of streamlit.

For application to run, database must be running locally and dependencies installed.

To install dependencies: (Best practice to create a virtual environment first) 'pip install -r requirements.txt'

To run the application: 'steamlit run bot.py'

Slides explaining the original application and future optimisations can be found at: 
https://docs.google.com/presentation/d/1WmJPYnvyyLaNWsLOjwuwy1qQumegAg9pnBtlpgj_ghY/edit#slide=id.p1


