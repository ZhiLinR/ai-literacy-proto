from const import VECTOR_STORES
from .email import SUMMARISE_AND_EMAIL

# Inbuilt OpenAI Tool Calls
FILE_SEARCH = {
    "type": "file_search",
    "vector_store_ids": VECTOR_STORES
}

WEB_SEARCH =  {
    "type": "web_search",
    "filters": {
        "allowed_domains": [
            "www.judiciary.gov.sg",
            "libguides.nus.edu.sg"
        ]
    }
}

TOOLS = [SUMMARISE_AND_EMAIL, FILE_SEARCH]