# multiplayer coinflip game
class CoinflipStats:
    NAME = "cf_stats"
    
    def __init__(self, games_won: int = 0, games_lost: int = 0, money_won: int = 0, money_lost: int = 0, most_lost: int = 0, most_lost_to_id: int = 0, loss_streak: int = 0):
        self.games_won = games_won
        self.games_lost = games_lost
        self.money_won = money_won
        self.money_lost = money_lost
        self.most_lost = most_lost
        self.most_lost_to_id = most_lost_to_id
        self.loss_streak = loss_streak
    
    def to_dict(self) -> dict[str, int | str]:
        return {
            "games_won": self.games_won,
            "games_lost": self.games_lost,
            "money_won": self.money_won,
            "money_lost": self.money_lost,
            "most_lost": self.most_lost,
            "most_lost_to_id": self.most_lost_to_id,
            "loss_streak": self.loss_streak
        }
    
    @staticmethod
    def from_dict(data: dict[str, int | str]) -> "CoinflipStats":
        return CoinflipStats(
            games_won=data.get("games_won", 0),
            games_lost=data.get("games_lost", 0),
            money_won=data.get("money_won", 0),
            money_lost=data.get("money_lost", 0),
            most_lost=data.get("most_lost", 0),
            most_lost_to_id=data.get("most_lost_to_id", 0),
            loss_streak=data.get("loss_streak", 0)
        )

    def modify(self, games_won: int = 0, games_lost: int = 0, money_won: int = 0, money_lost: int = 0, most_lost: int = 0, most_lost_to_id: int = 0, loss_streak: int = 0):
        self.games_won += games_won
        self.games_lost += games_lost
        self.money_won += money_won
        self.money_lost += money_lost
        self.most_lost = max(self.most_lost, most_lost)
        self.most_lost_to_id = most_lost_to_id
        self.loss_streak = loss_streak

# singleplayer mines game
class MinesStats:
    NAME = "mines_stats"

    def __init__(self, games_won: int = 0, games_lost: int = 0, money_won: int = 0, money_lost: int = 0):
        self.games_won = games_won
        self.games_lost = games_lost
        self.money_won = money_won
        self.money_lost = money_lost
    
    def to_dict(self) -> dict[str, int | str]:
        return {
            "games_won": self.games_won,
            "games_lost": self.games_lost,
            "money_won": self.money_won,
            "money_lost": self.money_lost
        }

    @staticmethod
    def from_dict(data: dict[str, int | str]) -> "MinesStats":
        return MinesStats(
            games_won=data.get("games_won", 0),
            games_lost=data.get("games_lost", 0),
            money_won=data.get("money_won", 0),
            money_lost=data.get("money_lost", 0)
        )

    def modify(self, games_won: int = 0, games_lost: int = 0, money_won: int = 0, money_lost: int = 0):
        self.games_won += games_won
        self.games_lost += games_lost
        self.money_won += money_won
        self.money_lost += money_lost