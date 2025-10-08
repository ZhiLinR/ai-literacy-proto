from datetime import date, datetime

from dateutil.relativedelta import relativedelta
import requests
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

from const import CALENDLY_USER_ID, CALENDLY_AUTH_TOKEN, CALENDLY_BASE


CREATE_CALENDAR_EVENT = {
        "type": "function",
        "name": "schedule_appointment",
        "description": "This tool is to schedule an appointment using Calendly.",
        "parameters": {
            "type": "object",
            "properties": {
                "create_event": {
                    "type": "string",
                    "description": "A boolean value which determines if the appointment should be created",
                },
                "event_name":{
                    "type": "string",
                    "description": "Short event name for the Calendly appointment. (less than 10 words)",
                }
            },
            "required": ["create_event","event_name"],
        },
    }
class CalendlyToolCallResponse(BaseModel):
    create_event: bool
    event_name: str
    
# Simple Implementation of the Response Body, only contains information we need
class _Event(BaseModel):
    name: str
    scheduling_url: HttpUrl
    uri: HttpUrl

class _CalendlyCreatedEventResponse(BaseModel):
    resource: _Event

class CalendlyEvent(BaseModel):
    # event_name: str
    uri: Optional[HttpUrl] = None
    
    def create_event(self, event_name)  -> dict :
        url = f"{CALENDLY_BASE}/one_off_event_types"
        
        start_date = date.today()
        # add 1 month to get the end date
        end_date = start_date + relativedelta(months=1)

        payload = {
            "name": event_name,
            "host": f"{CALENDLY_BASE}/users/{CALENDLY_USER_ID}",
            "duration": 45,
            "timezone": "Asia/Singapore",
            "date_setting": {
                "type": "date_range",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
            },
            "location": {
                "kind": "physical",
                "location": "Meowdy Legal Services Main Office @ SMU YPHSL SR 3-11"
            }
        }
        headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {CALENDLY_AUTH_TOKEN}"
        }
        response = requests.request("POST", url, json=payload, headers=headers).json()

        calendly_response = _CalendlyCreatedEventResponse.model_validate(response)
        
        text = f"""Please book your appointment at this [Calendly link]({calendly_response.resource.scheduling_url}). Once complete, please come back to this window and I will send the email with your case summary to our legal team."""
        return {"text": text, "scheduling_url": calendly_response.resource.scheduling_url}
    
        # return teZxt
    
    # def poll_event():
    #     url = "https://api.calendly.com/scheduled_events/uuid"

    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": ""
    #     }

    #     response = requests.request("GET", url, headers=headers)





