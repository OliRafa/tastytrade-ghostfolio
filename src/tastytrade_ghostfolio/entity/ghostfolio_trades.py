from tastytrade_ghostfolio.models.ghostfolio_activity import GhostfolioActivity


class GhostfolioTrades:
    def __init__(self, activities: list[GhostfolioActivity]):
        self.activities = activities

    def add_account_info(self, account_id: str):
        for activity in self.activities:
            activity.account_id = account_id
            activity.comment = "Activity created by Tastytrade-Ghostfolio."

    def adapt_symbols(self, symbol_mappings: dict[str, str]):
        for activity in self.activities:
            activity.symbol = symbol_mappings.get(activity.symbol, activity.symbol)
