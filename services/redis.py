from langchain_redis import RedisChatMessageHistory
from config import config

REDIS_URL = config["redis"]["url"]


class HistoryService:

    def __init__(self):
        self.redis_url = REDIS_URL

    def get_session(
        self,
        session_id: str,
    ) -> RedisChatMessageHistory:

        return RedisChatMessageHistory(
            session_id=session_id,
            redis_url=self.redis_url,
        )
    
    def add_user_message(
        self,
        session_id: str,
        message: str,
    ):

        history = self.get_session(session_id)

        history.add_user_message(message)

    def add_ai_message(
        self,
        session_id: str,
        message: str,
    ):

        history = self.get_history(session_id)

        history.add_ai_message(message)

    def save_conversation(
        self,
        session_id: str,
        question: str,
        answer: str,
    ):

        history = self.get_session(session_id)

        history.add_user_message(question)

        history.add_ai_message(answer)

    

history_service = HistoryService()