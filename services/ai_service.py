
"""Gemini AI service for INFINITY."""

import os
from services.event_service import get_published_events
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"

SYSTEM_INSTRUCTION = """
You are INFINITY AI Assistant for INFINITY - The Tech Society
at SGGSCC.

Your job:
- Explain INFINITY and its technology activities.
- Help visitors understand event registration.
- Answer questions about events, workshops and society activities.
- Guide users to the Events, Gallery and Contact sections.

Rules:
- Be friendly, helpful and professional.
- Keep answers clear and reasonably short.
- Support English and Hinglish.
- Never invent event dates, fees or official announcements.
- Do not claim to register anyone yourself.
- For unknown official information, direct visitors to the Contact section.
- Always use plain text formatting.
- Do not use Markdown symbols such as **, *, or #.
- Present event details in clean, readable lines.
"""

def ask_infinity(message, history=None):

    message = (message or "").strip()

    if not message:
        return {
            "success": False,
            "reply": "Please enter a message."
        }

    if len(message) > 2000:
        return {
            "success": False,
            "reply": "Please keep your message under 2000 characters."
        }

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "reply": "AI assistant is not configured."
        }
        # Fetch live published events from SQL Server
    event_result = get_published_events()

    event_context = ""

    if event_result["success"]:
        events = event_result["events"]

        if events:
            event_context = "\n\nCURRENT EVENTS FROM INFINITY DATABASE:\n"

            for event in events:
                event_date = event.get("EventDate")

                if event_date:
                    event_date = event_date.strftime("%d %B %Y")
                else:
                    event_date = "Date to be announced"

                event_context += (
                    f"- Event: {event.get('Title')}\n"
                    f"  Category: {event.get('Category')}\n"
                    f"  Date: {event_date}\n"
                    f"  Venue: {event.get('Venue')}\n"
                )
        else:
            event_context = "\nNo published events are currently listed."

    current_instruction = (
        SYSTEM_INSTRUCTION
        + event_context
        + "\nOnly share event details present in this database context."
    )
    client = None

    try:
        client = genai.Client(api_key=api_key)

        contents = []

        # Include recent conversation history
        for item in (history or [])[-8:]:

            role = item.get("role")
            text = item.get("text", "")

            if role in ("user", "model") and text:
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part.from_text(text=text)]
                    )
                )

        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=message)]
            )
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=current_instruction,
                temperature=0.5,
                max_output_tokens=400
            )
        )

        reply = (response.text or "").strip()

        if not reply:
            reply = "Please try asking your question again."

        return {
            "success": True,
            "reply": reply
        }

    except Exception as error:

        print("INFINITY AI ERROR:", repr(error))

        return {
            "success": False,
            "reply": "Sorry, AI is temporarily unavailable. Please try again."
        }

    finally:
        if client:
            client.close()
