from typing import Optional, Dict, Callable
from core.utils import log
from core.telegram_api import TelegramApi
from core.bot_state import BotState, BotResponse
from core.message import Message
from core.callback_query import CallbackQuery
from core.command import Command
from core.bot_state_logging_wrapper import BotStateLoggingWrapper
from trivia.bijection import Bijection
from dataclasses import dataclass, field
from core.utils import JsonDict
from trivia.telegram_models import Update


class Bot:
    """
        Обрабатывает полученные команды и сообщения от пользователя
    """

    @dataclass
    class State:
        """
        Вспомогательный класс для хранения парамметров class InGameState
        :param last_update_id: идентификатор последнего обновления
        :param chat_state: словарь для хранения состояния бота
        """
        chat_states: Dict[int, BotState] = field(default_factory=dict)

    def __init__(self,
                 telegram_api: TelegramApi,
                 create_initial_state: Callable[[], BotState],
                 state_to_dict_bijection: Bijection[BotState, JsonDict],
                 state: State = State()
                 ):
        self.telegram_api = telegram_api
        self.create_initial_state = create_initial_state
        self.state_to_dict_bijection = state_to_dict_bijection
        self.state = state

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"""
                Bot:
                    telegram_api = {self.telegram_api}
                    create_initial_state = {self.create_initial_state}
                    state_to_dict_bijection = {self.state_to_dict_bijection}
                    state = {self.state}
                """

    def process_updates(self, update: Update) -> None:
        """
           Обрабатывает полученные команды и сообщения от пользователя
        :return: None
        """
        chat_id = update.get_chat_id(update)
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

    def process_update(self, update: Update, state: BotState) -> Optional[BotResponse]:
        if update.message:
            chat_id = update.get_chat_id(update)
            message_text = update.message.text
            log(f"chat_id : {chat_id}. text: {message_text} ")
            if message_text.startswith("/"):
                user_command = Command(chat_id, message_text)
                bot_response: Optional[BotResponse] = state.process_command(user_command)
                return bot_response
            else:
                user_message = Message(chat_id, message_text)
                bot_response = state.process_message(user_message)
                return bot_response
        elif update.callback_query:
            callback_query_id = update.callback_query.id
            chat_id = update.callback_query.message.chat.id
            message_text = update.callback_query.message.text
            message = Message(chat_id, message_text)
            callback_query_data = update.callback_query.data
            message_id = update.callback_query.message.message_id
            callback_query = CallbackQuery(callback_query_data, message, message_id)
            self.telegram_api.answer_callback_query(callback_query_id)
            bot_response = state.process_callback_query(callback_query)
            return bot_response
        else:
            log("skipping update")
            return None

    def save(self) -> JsonDict:
        """
        Сохраняет состояние в словарь. Словарь может быть использован для дальнейшего восстановления
        :return: dict
        """
        dict_to_state = {}
        for chat_id, state in self.state.chat_states.items():
            dict_to_state[str(chat_id)] = self.state_to_dict_bijection.forward(state)

        return dict_to_state

    def load(self, data: JsonDict) -> None:
        """
        Загружает состояние из сохраненного ранее словаря
        :param data: dict
        :return: None
        """
        state = Bot.State()
        for chat_id, st in data.items():
            state.chat_states[int(chat_id)] = self.state_to_dict_bijection.backward(st)
        self.state = state

    def _get_state_for_chat(self, chat_id: int) -> BotState:
        if chat_id in self.state.chat_states:
            state = self.state.chat_states[chat_id]
        else:
            state = self.create_initial_state()
            self.state.chat_states[chat_id] = state
        return state
