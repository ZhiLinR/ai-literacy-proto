from const import OPENAI_CLIENT, PASSWORD
from tools.tools import TOOLS
from tools.email import MailgunEmail
import chainlit as cl

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("guest", PASSWORD):
        return cl.User(
            identifier="guest", metadata={"role": "guest", "provider": "credentials"}
        )
    else:
        return None



@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="GPT-5-nano",
            markdown_description="This is a test of a chatbot which responds to probono enquiries. It uses Singapore Divorce Court Law references as it's grounding information so it may not respond entirely correctly for other enquiries. Sessions only persist in this window, thank you for trying it.",
            icon="https://i.redd.it/kg82lbnu0ste1.png",
        )
    ]
    
# Chainlit interface
@cl.on_message
async def on_message(message: cl.Message):
    history  = cl.chat_context.to_openai()
    # Call OpenAI API to get a response
    response = OPENAI_CLIENT.responses.create(
        model="gpt-5-nano",
        instructions="You are a friendly assistant at a probono law firm in Singapore. Your job is to ONLY collect information so that your superiors can verify the validity of the case from a client. Do not ask the individual for personally identifiable information such as their NRIC. If there is missing information, prompt the client for them before proceeding. Always assume that the client is based in Singapore. You should not make any reccomendations. You are unable to handle file information. Try to keep your responses short (200 words) and gather just enough information to create a case summary. You should determine the end of a conversation and send an email at the end of your conversation to your firm (which is a tool call).",
        input=history,
        stream=True,
        tools=TOOLS
    )

    msg = cl.Message(content="")
    for event in response:
        if event.type == 'response.output_text.delta':
            await msg.stream_token(event.delta)
        elif event.type == 'response.function_call_arguments.done':
            # print(vars(event))
            email = MailgunEmail.model_validate_json(event.arguments)
            if email.send:
                email.send_simple_message(chat_log=history)
            # print(event.item.arguments)
            await msg.stream_token(email.template)
        else:
            continue
    
    await msg.update()

# Start the Chainlit app (interactive messaging interface)
if __name__ == "__main__":
    cl.run()

