from agents.application.executor import Executor as Agent
from agents.polymarket.gamma import GammaMarketClient as Gamma
from agents.polymarket.polymarket import Polymarket
from agents.connectors.polymarket_db import PolymarketDb

import shutil
import traceback
import sys

from agents.utils.objects import ActivityUser, TradedUser

from typing import Literal
from datetime import datetime

from rich import print
from rich.panel import Panel

class Trader:
    def __init__(self):
        self.polymarket = Polymarket()
        self.gamma = Gamma()
        self.agent = Agent()
        self.db = PolymarketDb()

    def pre_trade_logic(self) -> None:
        self.clear_local_dbs()

    def clear_local_dbs(self) -> None:
        try:
            shutil.rmtree("local_db_events")
        except:
            pass
        try:
            shutil.rmtree("local_db_markets")
        except:
            pass

    def one_best_trade(self) -> None:
        """

        one_best_trade is a strategy that evaluates all events, markets, and orderbooks

        leverages all available information sources accessible to the autonomous agent

        then executes that trade without any human intervention

        """
        self.pre_trade_logic()

        while True:
            try:
                
                events = self.polymarket.get_all_tradeable_events()
                print(Panel(f"1. FOUND {events} EVENTS", expand=False))

                filtered_events = self.agent.filter_events_with_rag(events)
                print(Panel(f"2. FILTERED {len(filtered_events)} EVENTS", expand=False))

                markets = self.agent.map_filtered_events_to_markets(filtered_events)
                print()
                print(Panel(f"3. FOUND {len(markets)} MARKETS", expand=False))

                print()
                filtered_markets = self.agent.filter_markets(markets)
                print(Panel(f"4. FILTERED {len(filtered_markets)} MARKETS", expand=False))

                market = filtered_markets[0]
                best_trade = self.agent.source_best_trade(market)
                print(Panel(f"5. CALCULATED TRADE {best_trade}", expand=False))

                if "not" in best_trade:
                    continue
                else:
                    amount = self.agent.format_trade_prompt_for_execution(best_trade)
                    print(f"amount: {amount}")
                    break
                # Please refer to TOS before uncommenting: polymarket.com/tos
                # trade = self.polymarket.execute_market_order(market, amount)
                # print(f"6. TRADED {trade}")

            except Exception as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                error_message = f"{exc_type.__name__}: {exc_value}"
                
                print(f"[red]{error_message}")
                formatted_exc = traceback.format_exception(exc_type, exc_value, exc_traceback)
                for line in formatted_exc:
                    print(f"[red]{line}")


    def maintain_positions(self):
        pass

    def incentive_farm(self):
        pass

    
    def _store_trader_data(self, trader_address: str) -> None:
        """  """
        activity_user = self.polymarket.get_proxy_addr_activity(trader_address)
        for obj in activity_user:
            self.db.write_activity_user(obj)

        positions = self.polymarket.get_proxy_addr_positions(trader_address)
        for obj in positions:
            self.db.write_user_position(obj)

        # traded_user = self.polymarket.get_proxy_addr_traded_user(trader_address)
        # self.db.write_traded_user(traded_user[0])

        # value_user = self.polymarket.get_proxy_addr_traded_user(trader_address)
        # self.db.write_value_user(value_user[0])


    def copy_trader(self, trader_address: str, epoch: Literal["y", "m", "d", "h"]) -> None:
        """ copy trades based on a trader's activity from the past epoch """
        
        self._store_trader_data(trader_address)
        cur_time = datetime.now()

        balance = self.polymarket.get_available_funds() 
        
        if not balance:
            raise Exception(f"Insufficient funds found at {self.polymarket.client.get_address()}")

        if "y" == epoch:
            cur_time = int(cur_time.replace(year=cur_time.year - 1).timestamp())
            activity = self.db.read_activity_positions_by_user_timestamp(cur_time)
        elif "m" == epoch:
            cur_time = int(cur_time.replace(month=cur_time.month - 1).timestamp())
            activity = self.db.read_activity_positions_by_user_timestamp(cur_time)
        elif "d" == epoch:
            cur_time = int(cur_time.replace(day=cur_time.day - 1).timestamp())
            activity = self.db.read_activity_positions_by_user_timestamp(cur_time)
        elif "h" == epoch:
            cur_time = int(cur_time.replace(hour=cur_time.hour - 1).timestamp())
            activity = self.db.read_activity_positions_by_user_timestamp(cur_time)
        else:
            raise ValueError(f"Invalid epoch value: {epoch}")
        
        for obj in activity:
            
            amount = obj.size if obj.size < balance else balance
            # market = self.polymarket.get_market(obj.asset)
            # create order
            trade = self.polymarket.execute_order(
                price=obj.price,
                size=amount,
                side=obj.side,
                token_id=obj.asset
            )

            print(Panel(f"order {trade}"))

        





        

        
        


                



if __name__ == "__main__":
    t = Trader()
    t.one_best_trade()
