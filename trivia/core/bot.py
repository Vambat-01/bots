from typing import Optional, Dict, Any, Callable
from core.utils import log
from core.telegram_api import TelegramApi
from core.bot_state import BotState, BotResponse
from core.message import Message
from core.callback_query import CallbackQuery
from core.command import Command
from core.bot_state_logging_wrapper import BotStateLoggingWrapper
from trivia.bijection import Bijection
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


class Bot:
    """
        Обрабатывает полученные команды и сообщения от пользователя
    """
    @dataclass_json
    @dataclass
    class State:
        last_update_id: int = 0
        chat_states: Dict[int, BotState] = field(default_factory=dict)

    def __init__(self, telegram_api: TelegramApi,
                 create_initial_state: Callable[[], BotState],
                 bijection: Bijection[BotState, dict],
                 state: State
                 ):
        self.telegram_api = telegram_api
        self.create_initial_state = create_initial_state
        self.bijection = bijection
        self.state = state

    def process_updates(self) -> None:
        """
           Обрабатывает полученные команды и сообщения от пользователя
        :return: None
        """
        response = self.telegram_api.get_updates(self.state.last_update_id + 1)
        data = response.json()
        result = data["result"]
        for update in result:
            self.state.last_update_id = update["update_id"]
            chat_id = self._get_chat_id(update)
            state = self._get_state_for_chat(chat_id)
            bot_response = self.process_update(update, state)
            if bot_response is not None:
                if bot_response.message is not None:
                    self.telegram_api.send_message(bot_response.message.chat_id,
                                                   bot_response.message.text,
                                                   bot_response.message.parse_mode,
                                                   bot_response.message.keyboard
                                                   )

                if bot_response.message_edit is not None:
                    self.telegram_api.edit_message(bot_response.message_edit.chat_id,
                                                   bot_response.message_edit.message_id,
                                                   bot_response.message_edit.text,
                                                   bot_response.message_edit.parse_mode
                                                   )

                if bot_response.new_state is not None:
                    new_state: BotState = bot_response.new_state
                    wrapped_new_state = BotStateLoggingWrapper(new_state)
                    self.state.chat_states[chat_id] = wrapped_new_state
                    first_message = wrapped_new_state.on_enter(chat_id)
                    if first_message is not None:
                        self.telegram_api.send_message(first_message.chat_id,
                                                       first_message.text,
                                                       first_message.parse_mode,
                                                       first_message.keyboard
                                                       )

    def process_update(self, update: Dict[str, Any], state: BotState) -> Optional[BotResponse]:
        if "message" in update:
            chat_id = self._get_chat_id(update)
            message_text = update["message"]["text"]
            log(f"chat_id : {chat_id}. text: {message_text} ")
            if message_text.startswith("/"):
                user_command = Command(chat_id, message_text)
                bot_response: Optional[BotResponse] = state.process_command(user_command)
                return bot_response
            else:
                user_message = Message(chat_id, message_text)
                bot_response = state.process_message(user_message)
                return bot_response
        elif "callback_query" in update:
            callback_query_id = update["callback_query"]["id"]
            chat_id = update["callback_query"]["message"]["chat"]["id"]
            message_text = update["callback_query"]["message"]["text"]
            message = Message(chat_id, message_text)
            callback_query_data = update["callback_query"]["data"]
            message_id = update["callback_query"]["message"]["message_id"]
            callback_query = CallbackQuery(callback_query_data, message, message_id)
            self.telegram_api.answer_callback_query(callback_query_id)
            bot_response = state.process_callback_query(callback_query)
            return bot_response
        else:
            log("skipping update")
            return None

    def save(self) -> dict:
        return self.state.to_dict()    # type: ignore

    def load(self, data: dict) -> None:
        self.state = Bot.State.from_dict(data)  # type: ignore

    def _get_chat_id(self, update: Dict[str, Any]) -> int:
        if "callback_query" in update:
            chat_id = update["callback_query"]["message"]["chat"]["id"]
        else:
            chat_id = update["message"]["chat"]["id"]
        return chat_id

    def _get_state_for_chat(self, chat_id: int) -> BotState:
        if chat_id in self.state.chat_states:
            state = self.state.chat_states[chat_id]
        else:
            state = self.create_initial_state()
            self.state.chat_states[chat_id] = state
        return state
