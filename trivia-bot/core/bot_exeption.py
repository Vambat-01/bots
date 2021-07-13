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


class NotEnoughQuestionsException(Exception):
    """
    Ошибка нехватки нужного количества вопросов для бота
    """
    pass
