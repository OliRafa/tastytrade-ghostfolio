from tastytrade import Account, ProductionSession
from tastytrade.account import Transaction

from tastytrade_ghostfolio.adapters.trade import adapt_trades
from tastytrade_ghostfolio.configs.settings import Settings
from tastytrade_ghostfolio.models.ghostfolio_account import GhostfolioAccount
from tastytrade_ghostfolio.models.ghostfolio_activity import TransactionType
from tastytrade_ghostfolio.services.ghostfolio import GhostfolioService


def get_tastytrade_session() -> ProductionSession:
    return ProductionSession(Settings.Tastytrade.USERNAME, Settings.Tastytrade.PASSWORD)


def get_tastytrade_account_history(session: ProductionSession) -> list[Transaction]:
    account = Account.get_accounts(session)[0]
    return account.get_history(session)


def filter_trades(transactions: list[Transaction]) -> list[Transaction]:
    trades = []
    for transaction in transactions:
        if transaction.transaction_type == "Trade" or (
            transaction.transaction_type == "Receive Deliver"
            and transaction.transaction_sub_type == "Dividend"
        ):
            trades.append(transaction)

    return trades


# def filter_dividends(transactions: list[Transaction]) -> list[Transaction]:
#     dividends = []
#     for transaction in transactions:
#         if (
#             transaction.transaction_sub_type == "Dividend"
#             and transaction.transaction_type == "Money Movement"
#         ):
#             dividends.append(transaction)

#     return dividends


# def extract_activities_from_account(
#     activities, account_id: str
# ) -> list[GhostfolioActivity]:
#     activities = list(filter(lambda x: x["accountId"] == account_id, activities))
#     return list(map(lambda x: GhostfolioActivity(**x), activities))


# response = requests.get(
#     f"{Settings.Ghostfolio.BASE_URL}/export",
#     headers={"Authorization": bearer_token},
# )
# response_data = response.json()
# accounts = response_data.get("accounts")
# tastytrade_account = next(
#     filter(lambda x: x["name"].lower() in ["tastyworks", "tastytrade"], accounts)
# )
# # activities = extract_activities_from_account(
# # response_data["activities"], tastytrade_account["id"]
# # )


ghostfolio_service = GhostfolioService()
ghostfolio_accounts = ghostfolio_service.get_all_accounts()

try:
    tastytrade_account = next(
        filter(
            lambda x: x.name.lower() in ["tastytrade", "tastyworks"],
            ghostfolio_accounts,
        )
    )

except StopIteration:
    tastytrade_account = GhostfolioAccount(name="Tastytrade")
    tastytrade_account = ghostfolio_service.create_account(tastytrade_account)

session = get_tastytrade_session()
transactions = get_tastytrade_account_history(session)

trades = filter_trades(transactions)
activities = adapt_trades(trades)

for activity in activities:
    activity.account_id = tastytrade_account.account_id
    activity.comment = "Activity created by Tastytrade-Ghostfolio."

orders = ghostfolio_service.get_all_orders(tastytrade_account.account_id)
buy_orders = list(filter(lambda x: x.type == TransactionType.BUY, orders))

print("Started exporting activities to Ghostfolio...")
activities_for_exporting = []
for activity in activities:
    try:
        next(
            filter(
                lambda x: x.date == activity.date
                and x.quantity == activity.quantity
                and x.symbol == activity.symbol,
                buy_orders,
            )
        )
    except StopIteration:
        activities_for_exporting.append(activity)
ghostfolio_service.export_activities_to_ghostfolio(activities_for_exporting)
print("Done!")
