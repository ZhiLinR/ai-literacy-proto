from const import VECTOR_STORES
from .email import SUMMARISE_AND_EMAIL
from .calendly import CREATE_CALENDAR_EVENT

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

TOOLS = [FILE_SEARCH, SUMMARISE_AND_EMAIL, CREATE_CALENDAR_EVENT]