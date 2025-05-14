from __future__ import annotations

import typer
from typing import Literal
from typing_extensions import Annotated

from devtools import pprint

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from agents.polymarket.polymarket import Polymarket
from agents.connectors.chroma import PolymarketRAG
from agents.connectors.news import News
from agents.application.trade import Trader
from agents.application.executor import Executor
from agents.application.creator import Creator

from enum import Enum

app = typer.Typer()
polymarket = Polymarket()
newsapi_client = News()
polymarket_rag = PolymarketRAG()


@app.command()
def get_all_markets(limit: int = 5, sort_by: str = "spread") -> None:
    """
    Query Polymarket's markets
    """
    print(f"limit: int = {limit}, sort_by: str = {sort_by}")
    markets = polymarket.get_all_markets()
    markets = polymarket.filter_markets_for_trading(markets)
    if sort_by == "spread":
        markets = sorted(markets, key=lambda x: x.spread, reverse=True)
    markets = markets[:limit]
    pprint(markets)


@app.command()
def get_relevant_news(keywords: str) -> None:
    """
    Use NewsAPI to query the internet
    """
    articles = newsapi_client.get_articles_for_cli_keywords(keywords)
    pprint(articles)


@app.command()
def get_all_events(limit: int = 5, sort_by: str = "number_of_markets") -> None:
    """
    Query Polymarket's events
    """
    print(f"limit: int = {limit}, sort_by: str = {sort_by}")
    events = polymarket.get_all_events()
    events = polymarket.filter_events_for_trading(events)
    if sort_by == "number_of_markets":
        events = sorted(events, key=lambda x: len(x.markets), reverse=True)
    events = events[:limit]
    pprint(events)


@app.command()
def create_local_markets_rag(local_directory: str) -> None:
    """
    Create a local markets database for RAG
    """
    polymarket_rag.create_local_markets_rag(local_directory=local_directory)


@app.command()
def query_local_markets_rag(vector_db_directory: str, query: str) -> None:
    """
    RAG over a local database of Polymarket's events
    """
    response = polymarket_rag.query_local_markets_rag(
        local_directory=vector_db_directory, query=query
    )
    pprint(response)


@app.command()
def ask_superforecaster(event_title: str, market_question: str, outcome: str) -> None:
    """
    Ask a superforecaster about a trade
    """
    print(
        f"event: str = {event_title}, question: str = {market_question}, outcome (usually yes or no): str = {outcome}"
    )
    executor = Executor()
    response = executor.get_superforecast(
        event_title=event_title, market_question=market_question, outcome=outcome
    )
    print(f"Response:{response}")


@app.command()
def create_market() -> None:
    """
    Format a request to create a market on Polymarket
    """
    c = Creator()
    market_description = c.one_best_market()
    print(f"market_description: str = {market_description}")


@app.command()
def ask_llm(user_input: str) -> None:
    """
    Ask a question to the LLM and get a response.
    """
    executor = Executor()
    response = executor.get_llm_response(user_input)
    print(f"LLM Response: {response}")


@app.command()
def ask_polymarket_llm(user_input: str) -> None:
    """
    What types of markets do you want trade?
    """
    executor = Executor()
    response = executor.get_polymarket_llm(user_input=user_input)
    print(f"LLM + current markets&events response: {response}")


@app.command()
def run_autonomous_trader() -> None:
    """
    Let an autonomous system trade for you.
    """
    trader = Trader()
    trader.one_best_trade()

@app.command()
def top_traders(limit: int=50) -> None:
    """
    Find top active traders by cumulative profit margin and current value
    """
    top_traders = polymarket.get_top_active_traders(limit)
    table = Table(title="Top Traders on Polymarket")

    table.add_column("Name")
    table.add_column("Proxy Address")
    table.add_column("Amount")
    table.add_column("Current Value")
    table.add_column("# of Trades")

    for trader in top_traders:

        # get current amount

        # _value_user = polymarket.get_proxy_addr_value_user(trader.proxyWallet)
        # _traded_user = polymarket.get_proxy_addr_traded_user(trader.proxyWallet)
        
        table.add_row(
            trader.name, 
            trader.proxyWallet, 
            "{:.2f}".format(trader.amount),
            "{:.2f}".format(trader.current_value),
            str(trader.trades),    
        )

    console = Console()
    console.print()
    console.print(table)
    console.print()

class Epoch(str, Enum):
    year = "y"
    month = "m"
    day = "d"
    hour = "h"

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.progress import track

def addr_callback(ctx: typer.Context, value: str):
    if ctx.resilient_parsing:
        return
    
    # print("validating proxy address")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching top traders...", total=None)
        
        top_traders = polymarket.get_top_active_traders(30)
        progress.add_task(description="Validating address...", total=None)
        if value not in [trader.proxyWallet for trader in top_traders]:
            raise typer.BadParameter("Proxy address is not top 100 traders on Polymarket.")
        else:
            return value


@app.command()
def copy_trader(
    addr: str = typer.Option(
        prompt="wallet proxy address",
        help="Polymarket creates proxy address for each user",
        case_sensitive=False,
        callback=addr_callback
    ),
    epoch: 
        Epoch =
        typer.Option(
            ...,
            prompt=True,
            help="Time window: y=year, m=month, d=day, h=hour",
            show_choices=True,
            case_sensitive=False
        ),
):
    """
    Copy a trader’s activity for the given time window.
    """
    trader = Trader()
    trader.copy_trader(addr, epoch)



if __name__ == "__main__":
    app()
