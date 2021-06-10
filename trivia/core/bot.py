import logging
from typing import Optional, Callable
from core.telegram_api import TelegramApi
from core.bot_state import BotState, BotResponse
from core.message import Message
from core.callback_query import CallbackQuery
from core.command import Command
from core.bot_state_logging_wrapper import BotStateLoggingWrapper
from trivia.bijection import Bijection
from core.utils import JsonDict
from trivia.telegram_models import Update
from core.redis_api import RedisApi
from core.chat_state_storage import ChatStateStorage


class Bot:
    """
        Обрабатывает полученные команды и сообщения от пользователя
    """
    def __init__(self,
                 telegram_api: TelegramApi,
                 redis_api: RedisApi,
                 create_initial_state: Callable[[], BotState],
                 state_to_dict_bijection: Bijection[BotState, JsonDict],
                 chat_state_storage: ChatStateStorage
                 ):
        self.telegram_api = telegram_api
        self.redis_api = redis_api
        self.create_initial_state = create_initial_state
        self.state_to_dict_bijection = state_to_dict_bijection
        self.chat_state_storage = chat_state_storage

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
                    redis_api = {self.redis_api}
                    state_to_dict_bijection = {self.state_to_dict_bijection}
                    state = {self.chat_state_storage}
                """

    async def process_update(self, update: Update) -> None:
        """
           Обрабатывает полученные команды и сообщения от пользователя
        :return: None
        """
        chat_id = update.get_chat_id(update)
        await self.redis_api.lock(f"lock_{chat_id}")
        state = self.chat_state_storage.get_state(chat_id)
        if not state:
            state = self.create_initial_state()
        bot_response = await self._process_update(update, state)
        if bot_response is not None:
            if bot_response.message is not None:
                await self.telegram_api.send_message(bot_response.message.chat_id,
                                                     bot_response.message.text,
                                                     bot_response.message.parse_mode,
                                                     bot_response.message.keyboard
                                                     )

            if bot_response.message_edit is not None:
                await self.telegram_api.edit_message(bot_response.message_edit.chat_id,
                                                     bot_response.message_edit.message_id,
                                                     bot_response.message_edit.text,
                                                     bot_response.message_edit.parse_mode
                                                     )

            if bot_response.new_state is not None:
                state = BotStateLoggingWrapper(bot_response.new_state)
                first_message = state.on_enter(chat_id)
                if first_message is not None:
                    await self.telegram_api.send_message(first_message.chat_id,
                                                         first_message.text,
                                                         first_message.parse_mode,
                                                         first_message.keyboard
                                                         )
        self.chat_state_storage.set_state(chat_id, state)
        self.redis_api.unlock(f"lock_{chat_id}")

    async def _process_update(self, update: Update, state: BotState) -> Optional[BotResponse]:
        if update.message:
            if not update.message.text:
                raise InvalidUpdateException("Message text is not found")

            chat_id = update.get_chat_id(update)
            message_text = update.message.text
            logging.info(f"chat_id : {chat_id}. text: {message_text} ")

            if message_text.startswith("/"):
                user_command = Command(chat_id, message_text)
                bot_response: Optional[BotResponse] = state.process_command(user_command)
                return bot_response
            else:
                user_message = Message(chat_id, message_text)
                bot_response = state.process_message(user_message)
                return bot_response

        elif update.callback_query:
            if not update.callback_query.message:
                raise InvalidUpdateException("CallbackQuery message is not found")

            if not update.callback_query.data:
                raise InvalidUpdateException("CallbackQuery data is not found")

            if not update.callback_query.message.text:
                raise InvalidUpdateException("Message text is not found")
            callback_query_id = update.callback_query.id
            chat_id = update.callback_query.message.chat.id
            message_text = update.callback_query.message.text
            message = Message(chat_id, message_text)
            callback_query_data = update.callback_query.data
            message_id = update.callback_query.message.message_id
            callback_query = CallbackQuery(callback_query_data, message, message_id)
            await self.telegram_api.answer_callback_query(callback_query_id)
            bot_response = state.process_callback_query(callback_query)
            return bot_response
        else:
            logging.info("skipping update")
            return None


class BotException(Exception):
    """
    Ошибка обработки апдейта ботом
    """
    pass


class InvalidUpdateException(BotException):
    """
    Исключения для бота, когда пришло не правильное обновление и бот не может его обработать
    """
    pass
