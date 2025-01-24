from tastytrade_ghostfolio.infra.ghostfolio.ghostfolio_adapter import GhostfolioAdapter
from tastytrade_ghostfolio.infra.ghostfolio.ghostfolio_api import GhostfolioApi

adapter = GhostfolioAdapter(GhostfolioApi())
account = adapter.get_or_create_account()
old_orders = adapter._get_orders("2a7efb1f-8f3c-43de-8778-f8488f1719d3")
orders = adapter._get_orders(account.account_id)
print(orders)
