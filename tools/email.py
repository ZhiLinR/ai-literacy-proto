import requests
from const import MAILGUN_API_KEY, MAILGUN_SANDBOX_DOMAIN, MAILGUN_SANDBOX_USER
from pydantic import BaseModel
from typing import Optional

class MailgunEmail(BaseModel):
    recipient_email: str
    subject_line: str
    send: bool
    
    summary: str
    # details: str
    chat_log: Optional[str] = ""
     
    template: str = """Thank you for submitting your case details to us. We have received your information and our team will review your submission carefully. \n\nYou can expect to hear back from us within 3-5 working days regarding the next steps. If we require any additional information or clarification, we will reach out to you directly. \n\nIf your matter is urgent or involves immediate safety concerns, please contact the relevant authorities (e.g., the police at 999 in Singapore) or seek emergency assistance.\n\nWarm regards, \n\nMeowdy Pro Bono Legal Services Team
    """
    def send_simple_message(self, chat_log: list ):
        role_map = {
            "user": "[Client]",
            "assistant": "[Bot Assistant]",
            "system": "[System]"
        }

        formatted = []
        for msg in chat_log:
            role = role_map.get(msg["role"], f"[{msg['role'].capitalize()}]")
            formatted.append(f"{role} {msg['content']}")

        self.chat_log = f"{"<br>".join(formatted)}"
        
        print("Reached send_simple_message")
        return requests.post(
            MAILGUN_SANDBOX_DOMAIN,
            auth=("api", MAILGUN_API_KEY),
            data={"from": MAILGUN_SANDBOX_USER,
                "to": self.recipient_email,
                "subject": f"[Automated Case Inquiry] {self.subject_line}",
                "template": "default email",
                "h:X-Mailgun-Variables": self._format_message()
                })
    def _format_message(self):
        
        template_str = self.model_dump_json(exclude=["recipient_email","subject_line","send","template"])
        return template_str

SUMMARISE_AND_EMAIL = {
        "type": "function",
        "name": "get_summary_and_email",
        "description": "Prepare a concise summary of the conversation for creating a legal case. Use this function ONLY when the conversation has ended and neccessary details have been provided.",
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "A text summary of all information provided in the chat.",
                },
                # "details": {
                #     "type": "string",
                #     "description": "A point form, separated list of facts about the client in denoted with the <pre> tag.",
                # },
                "send": {
                    "type": "string",
                    "description": "A boolean value which determines if the summary is ready to be sent. Returns true or false ONLY.",
                },
                "recipient_email": {
                    "type": "string",
                    "description": "A string value of the user's email. If not provided, ask the user for it.",
                },
                "subject_line": {
                    "type": "string",
                    "description": "A short email subject line less than 20 words.",
                }
            },
            "required": ["summary","send","recipient_email"],
        },
    }