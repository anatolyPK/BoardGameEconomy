from models.base import User
from schemas.portfolio import GeneralInfoSchema
from schemas.transactions import GameTransactionsSchema


def get_users_games_general_info(games_schema: GameTransactionsSchema, user: User):
    games = games_schema.games
    if not games:
        return GeneralInfoSchema(
            username=user.username,
            game_in_stock=0,
            average_price_of_game_in_stock=0,
            amount_spent=0,
            game_transactions=None,
        )

    game_in_stock = sum(1 for game in games if not game.selling_price)
    amount_of_games_in_stock = sum(
        game.purchase_price for game in games if not game.selling_price
    )
    amount_of_selling_games = sum(
        game.selling_price - game.purchase_price for game in games if game.selling_price
    )
    total_amount = amount_of_games_in_stock + amount_of_selling_games
    average_price_of_game_in_stock = (
        amount_of_games_in_stock / game_in_stock if game_in_stock else 0
    )

    return GeneralInfoSchema(
        username=user.username,
        game_in_stock=game_in_stock,
        average_price_of_game_in_stock=average_price_of_game_in_stock,
        amount_spent=total_amount,
        game_transactions=games_schema,
    )
