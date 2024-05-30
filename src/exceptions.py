class GamesAreOver(Exception):
    """BGG API. Конец списка игр"""

    pass


class UnauthorizedTransactionError(Exception):
    """
    Транзакция игры не принадлежит текущему пользователю
    """

    def __init__(self, message="Transaction does not belong to the user"):
        self.message = message
        super().__init__(self.message)
