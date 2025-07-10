import os
import json 
from typing import TypedDict

from dotenv import load_dotenv
from imap_tools import MailBox, AND

from langchain.chat_models import init_chat_model
from langchain_core.tools import tool

from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph,START, END

load_dotenv()
# Load environment variables
IMAP_HOST ='imap.gmail.com'
IMAP_USER ='email_address'
IMAP_PASSWORD ='app_password'  # Use an app password if 2FA is enabled
IMAP_FOLDER = 'INBOX'

# CHAT_MODEL = 'qwen3:0.6b-q4_K_M'
CHAT_MODEL = 'qwen3:8b'

# This stores the chat messages
class ChatState(TypedDict):
    messages: list

# Connect to the IMAP server and return the mailbox object
def connect():
    """Connect to the IMAP server."""
    mailbox = MailBox(IMAP_HOST)
    mailbox.login(IMAP_USER, IMAP_PASSWORD, initial_folder=IMAP_FOLDER)
    return mailbox


# Tool 1: Fetches the latest unread emails
@tool
def list_unread_emails():
    """Return a bullet list of every unread message's UID, subject, date and sender"""
    print("List unread emails tool called")

    with connect() as mailbox:
        unread = list(mailbox.fetch(criteria = AND(seen=False),headers_only=True,mark_seen=False))

    if not unread:
        return "No unread emails found."
    
    response = json.dumps([
        {
            "uid": mail.uid,
            "date": mail.date.astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "subject": mail.subject,
            "sender": mail.from_,
        }for mail in unread
    ]) 

    return response


# Tool 2: Summarizes the latest unread email
@tool
def summarize_email(uid):
    """Summarize a single e-mail given it's IMAP UID. Return a short summary of the e-mails content / body in plain text"""

    with connect() as mailbox:
        mail = next(mailbox.fetch(AND(uid=uid),mark_seen=False),None)

    if not mail:
        return f"No email found with UID {uid}."
    
    prompt = (
        "Summarize this e-mail concisely:\n\n"
        f"Subject: {mail.subject}\n"
        f"Sender: {mail.from_}\n"
        f"Date: {mail.date}\n\n"
        f"{mail.text or mail.html}"
    )

    return raw_llm.invoke(prompt).content


# Agentic System Implementation
llm = init_chat_model(CHAT_MODEL, model_provider='ollama')

# Giving model tools to use
llm = llm.bind_tools([list_unread_emails, summarize_email])

# This raw llm is used to summarize the email content without tools 
raw_llm = init_chat_model(CHAT_MODEL, model_provider='ollama')


def llm_model(state):
    response = llm.invoke(state['messages'])
    return {'messages':state['messages']+[response]}

def router(state):
    last_message = state['messages'][-1]
    return 'tools' if getattr(last_message, 'tool_calls', None) else 'end'

tool_node = ToolNode([list_unread_emails, summarize_email])


def tools_node(state):
    result = tool_node.invoke(state)

    return {
        'messages': state['messages'] + result['messages']
    }

builder = StateGraph(ChatState)
builder.add_node('llm',llm_model)
builder.add_node('tools', tool_node)
builder.add_edge(START, 'llm')
builder.add_edge('tools','llm')
builder.add_conditional_edges('llm',router,{'tools':'tools', 'end':END})


graph  = builder.compile()

if __name__ == '__main__':
    state = {'messages':[]}

    print('Type an instruction or quit.\n')

    while True:
        user_message = input('> ')
        if user_message.lower() in ['quit', 'exit']:
            break
        state['messages'].append({'role': 'user', 'content': user_message})
        state = graph.invoke(state)
        print(state['messages'][-1].content)











