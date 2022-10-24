


import requests

from dataclasses import dataclass, asdict
import os
from dotenv import load_dotenv

load_dotenv()


HASURA_HEADERS = {"X-Hasura-Admin-Secret": os.getenv('HASURA_ADMIN_SECRET')}


################
# GRAPHQL CLIENT
################

@dataclass
class Client:
    url: str
    headers: dict

    def run_query(self, query: str, variables: dict, extract=False):
        request = requests.post(
            self.url,
            headers=self.headers,
            json={"query": query, "variables": variables},
        )
        assert request.ok, f"Failed with code {request.status_code}"
        return request.json()
    
    get_articles = lambda self: self.run_query(
        """
            query GetArticles {
                Article{
                    id
                    title
                }
            }
        """,
        {},
    )

    create_article = lambda self, idx, title: self.run_query(
        """
            mutation CreateArtile($idx: String!, $title: String!) {
                insert_Article_one(object: {id: $idx, title: $title}) {
                    id
                    
                }
            }
        """,
        {"idx": idx, "title": title},
    )


client = Client(url=os.getenv('HASURA_URL'), headers=HASURA_HEADERS)

#client.get_articles()






