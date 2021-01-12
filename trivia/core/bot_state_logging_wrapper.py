from typing import Optional
from core.bot_state import BotState, BotResponse
from core.utils import dedent_and_strip, log
from core.message import Message
from core.callback_query import CallbackQuery
from core.command import Command


class BotStateLoggingWrapper(BotState):
    def __init__(self, inner: BotState):
        self.inner = inner

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False

    def __repr__(self):
        return dedent_and_strip(f"""
                      BotStateLoggingWrapper: 
                          inner: {self.inner}
                   """)

    def __str__(self):
        return self.__repr__()

    def process_message(self, message: Message) -> BotResponse:
        log(f"{type(self.inner).__name__} process_message is called")
        return self.inner.process_message(message)

    def process_command(self, command: Command) -> BotResponse:
        log(f"{type(self.inner).__name__} process_command is called")
        return self.inner.process_command(command)

    def on_enter(self, chat_id: int) -> Optional[Message]:
        log(f"{type(self.inner).__name__} on_enter is called")
        return self.inner.on_enter(chat_id)

    def process_callback_query(self, callback_query: CallbackQuery) -> Optional[BotResponse]:
        log(f"{type(self.inner).__name__} callback_query is called")
        return self.inner.process_callback_query(callback_query)
