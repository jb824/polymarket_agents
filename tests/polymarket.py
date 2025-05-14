from agents.polymarket.polymarket import Polymarket, PolymarketDb
from agents.application.trade import Trader

def get_user_activity_test(db: PolymarketDb, user: str):    
    pm = Polymarket()
    activity_user = pm.get_proxy_addr_activity(proxy_address=user, limit=1000)
    for activity in activity_user:
        db.write_activity_user(activity)

def get_user_positions_test(db: PolymarketDb, user: str) -> None:
    pm = Polymarket()
    user_position = pm.get_proxy_addr_positions(proxy_address=user)
    for position in user_position:
        db.write_user_position(position)

def get_traded_user_test(db: PolymarketDb, user: str) -> None:
    pm = Polymarket()
    traded_user = pm.get_proxy_addr_traded_user(user)
    for trades in traded_user:
        db.write_traded_user(trades)

def get_all_markets_test():
    pm = Polymarket()
    markets = pm.get_all_markets()
    for market in markets:
        print(market)

def copy_trader_test(addr: str, epoch: str):
    trade = Trader()
    trade.copy_trader(addr, epoch)


def main():
    PROXY_WALLET = "0x44c1dfe43260c94ed4f1d00de2e1f80fb113ebc1"

    db = PolymarketDb()
    db.create_db_tables()

    # get_user_activity_test(db, PROXY_WALLET)
    # get_user_positions_test(db, PROXY_WALLET)

    # get_all_markets_test()

    copy_trader_test(PROXY_WALLET, "d")

    db.close()


if __name__ == "__main__":
    main()
