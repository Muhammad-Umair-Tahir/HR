# hr_ai.py
import os
from google import genai
from google.genai import types
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.memory.chat_message_histories import ChatMessageHistory
import dotenv

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
DEFAULT_LLM_MODEL = "models/gemini-2.5-flash"

INSTRUCTIONS = """You are a HR assistant for a university named University of Management and Technology. Greet the people with educational way but if anyone asks for some extra info say that the platform is under development and will be available soon. Do not tell your capabilities for now and with every answer include the under development message."""

# Global session memory store (in-memory)
session_memories = {}

class HR_AI:
    def __init__(self, model_name: str = DEFAULT_LLM_MODEL):
        self.model_name = model_name
        self.client_genai = self._get_genai_client()

    def _get_genai_client(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set.")
        return genai.Client(api_key=GEMINI_API_KEY)

    def _get_memory(self, session_id: str):
        if session_id not in session_memories:
            session_memories[session_id] = ConversationBufferMemory(
                return_messages=True
            )
        return session_memories[session_id]

    async def generate(self, user_message: str, session_id: str = "default"):
        print(f"User: {user_message}")
        memory = self._get_memory(session_id)
        history = memory.chat_memory.messages

        # Prepare contents for Gemini
        contents = []
        for msg in history:
            if isinstance(msg, HumanMessage):
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=msg.content)]))
            elif isinstance(msg, AIMessage):
                contents.append(types.Content(role="model", parts=[types.Part.from_text(text=msg.content)]))

        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

        config = types.GenerateContentConfig(
            system_instruction=INSTRUCTIONS,
        )

        full_response = ""
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            response_stream = await loop.run_in_executor(
                None,
                lambda: self.client_genai.models.generate_content_stream(
                    model=self.model_name,
                    contents=contents,
                    config=config
                )
            )
            for chunk in response_stream:
                full_response += chunk.text
                print(chunk.text, end="")
            print()

        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred."

        # Save turn in LangChain memory
        memory.chat_memory.add_user_message(user_message)
        memory.chat_memory.add_ai_message(full_response)

        return full_response
