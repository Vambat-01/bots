class Command:
    """
        Телеграм команда
    """

    def __init__(self, chat_id: int, text: str):
        self.chat_id = chat_id
        self.text = text

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__dict__ == other.__dict__
        return False
