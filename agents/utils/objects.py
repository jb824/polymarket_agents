from __future__ import annotations
from typing import Optional, Union, Literal
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Trade(BaseModel):
    id: int
    taker_order_id: str
    market: str
    asset_id: str
    side: str
    size: str
    fee_rate_bps: str
    price: str
    status: str
    match_time: str
    last_update: str
    outcome: str
    maker_address: str
    owner: str
    transaction_hash: str
    bucket_index: str
    maker_orders: list[str]
    type: str


class SimpleMarket(BaseModel):
    id: int
    question: str
    # start: str
    end: str
    description: str
    active: bool
    # deployed: Optional[bool]
    funded: bool
    # orderMinSize: float
    # orderPriceMinTickSize: float
    rewardsMinSize: float
    rewardsMaxSpread: float
    # volume: Optional[float]
    spread: float
    outcomes: str
    outcome_prices: str
    clob_token_ids: Optional[str]
    condition_id: str
    question_id: str


class ClobReward(BaseModel):
    id: str  # returned as string in api but really an int?
    conditionId: str
    assetAddress: str
    rewardsAmount: float  # only seen 0 but could be float?
    rewardsDailyRate: int  # only seen ints but could be float?
    startDate: str  # yyyy-mm-dd formatted date string
    endDate: str  # yyyy-mm-dd formatted date string


class Tag(BaseModel):
    id: str
    label: Optional[str] = None
    slug: Optional[str] = None
    forceShow: Optional[bool] = None  # missing from current events data
    createdAt: Optional[str] = None  # missing from events data
    updatedAt: Optional[str] = None  # missing from current events data
    _sync: Optional[bool] = None


class PolymarketEvent(BaseModel):
    id: str  # "11421"
    ticker: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    startDate: Optional[str] = None
    creationDate: Optional[str] = (
        None  # fine in market event but missing from events response
    )
    endDate: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None
    active: Optional[bool] = None
    closed: Optional[bool] = None
    archived: Optional[bool] = None
    new: Optional[bool] = None
    featured: Optional[bool] = None
    restricted: Optional[bool] = None
    liquidity: Optional[float] = None
    volume: Optional[float] = None
    reviewStatus: Optional[str] = None
    createdAt: Optional[str] = None  # 2024-07-08T01:06:23.982796Z,
    updatedAt: Optional[str] = None  # 2024-07-15T17:12:48.601056Z,
    competitive: Optional[float] = None
    volume24hr: Optional[float] = None
    enableOrderBook: Optional[bool] = None
    liquidityClob: Optional[float] = None
    _sync: Optional[bool] = None
    commentCount: Optional[int] = None
    # markets: list[str, 'Market'] # forward reference Market defined below - TODO: double check this works as intended
    markets: Optional[list[Market]] = None
    tags: Optional[list[Tag]] = None
    cyom: Optional[bool] = None
    showAllOutcomes: Optional[bool] = None
    showMarketImages: Optional[bool] = None


class Market(BaseModel):
    id: int
    question: Optional[str] = None
    conditionId: Optional[str] = None
    slug: Optional[str] = None
    resolutionSource: Optional[str] = None
    endDate: Optional[str] = None
    liquidity: Optional[float] = None
    startDate: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    outcome: Optional[list] = None
    outcomePrices: Optional[list] = None
    volume: Optional[float] = None
    active: Optional[bool] = None
    closed: Optional[bool] = None
    marketMakerAddress: Optional[str] = None
    createdAt: Optional[str] = None  # date type worth enforcing for dates?
    updatedAt: Optional[str] = None
    new: Optional[bool] = None
    featured: Optional[bool] = None
    submitted_by: Optional[str] = None
    archived: Optional[bool] = None
    resolvedBy: Optional[str] = None
    restricted: Optional[bool] = None
    groupItemTitle: Optional[str] = None
    groupItemThreshold: Optional[int] = None
    questionID: Optional[str] = None
    enableOrderBook: Optional[bool] = None
    orderPriceMinTickSize: Optional[float] = None
    orderMinSize: Optional[int] = None
    volumeNum: Optional[float] = None
    liquidityNum: Optional[float] = None
    endDateIso: Optional[str] = None  # iso format date = None
    startDateIso: Optional[str] = None
    hasReviewedDates: Optional[bool] = None
    volume24hr: Optional[float] = None
    clobTokenIds: Optional[list] = None
    umaBond: Optional[int] = None  # returned as string from api?
    umaReward: Optional[int] = None  # returned as string from api?
    volume24hrClob: Optional[float] = None
    volumeClob: Optional[float] = None
    liquidityClob: Optional[float] = None
    acceptingOrders: Optional[bool] = None
    negRisk: Optional[bool] = None
    commentCount: Optional[int] = None
    _sync: Optional[bool] = None
    events: Optional[list[PolymarketEvent]] = None
    ready: Optional[bool] = None
    deployed: Optional[bool] = None
    funded: Optional[bool] = None
    deployedTimestamp: Optional[str] = None  # utc z datetime string
    acceptingOrdersTimestamp: Optional[str] = None  # utc z datetime string,
    cyom: Optional[bool] = None
    competitive: Optional[float] = None
    pagerDutyNotificationEnabled: Optional[bool] = None
    reviewStatus: Optional[str] = None  # deployed, draft, etc.
    approved: Optional[bool] = None
    clobRewards: Optional[list[ClobReward]] = None
    rewardsMinSize: Optional[int] = (
        None  # would make sense to allow float but we'll see
    )
    rewardsMaxSpread: Optional[float] = None
    spread: Optional[float] = None


class ComplexMarket(BaseModel):
    id: int
    condition_id: str
    question_id: str
    tokens: Union[str, str]
    rewards: str
    minimum_order_size: str
    minimum_tick_size: str
    description: str
    category: str
    end_date_iso: str
    game_start_time: str
    question: str
    market_slug: str
    min_incentive_size: str
    max_incentive_spread: str
    active: bool
    closed: bool
    seconds_delay: int
    icon: str
    fpmm: str
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


class SimpleEvent(BaseModel):
    id: int
    ticker: str
    slug: str
    title: str
    description: str
    end: str
    active: bool
    closed: bool
    archived: bool
    restricted: bool
    new: bool
    featured: bool
    restricted: bool
    markets: str


class Source(BaseModel):
    id: Optional[str]
    name: Optional[str]


class Article(BaseModel):
    source: Optional[Source]
    author: Optional[str]
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    urlToImage: Optional[str]
    publishedAt: Optional[str]
    content: Optional[str]

class Vote(BaseModel):
    id: Optional[str]
    requester: Optional[str]
    identifier: Optional[str]
    timestamp: Optional[int]


class ValueUser(BaseModel):
    """
    https://data-api.polymarket.com/value?user={proxy wallet address}

    attributes:
        user (str): user proxy address
        value (float): current amount from proxy address 
    
    """
    user: str
    value: float

class TradedUser(BaseModel, frozen=True):
    """ 
    https://data-api.polymarket.com/traded?user={proxy wallet address}

    attributes:
        user (str): user proxy address
        traded (int): total markets traded
    """
    user: str
    traded: int 

class ActivityUser(BaseModel, frozen=True):
    """
    https://data-api.polymarket.com/activity?user={proxy wallet address}&limit=100&offset=0

    attributes: 
        proxyWallet (str): user proxy address
        timestamp (int): unix format 
        conditionId (str): condition that the token is linked to
        type (str): specify transaction type (e.g., 'TRADE', 'REDEEM')
        size (float): number of shares
        usdcSize (float):
        transactionHash (str): 
        price (float):
        asset (str): token id associated with transaction
        side (str):
        outcomeIndex (int):
        title (str): event name
        slug (str): event slug
        icon (str): url to event image
        eventSlug (str): event slug
        outcome (str): returns readable "Yes" or "No"
        name (str): account username
        pseudonym (str): pseudonym name associated with account 
        bio (str): 
        profileImage (str): url of account profile picture
        profileImageOptimized (str):
    """
    proxyWallet: str 
    timestamp: int
    conditionId: str
    type: str
    size: float
    usdcSize: float
    transactionHash: str
    price: float
    asset: str
    side: str
    outcomeIndex: int
    title: str
    slug: str
    icon: str
    eventSlug: str
    outcome: str
    name: str
    pseudonym: str
    bio: str
    profileImage: str
    profileImageOptimized: str

    model_config = ConfigDict(extra="ignore")      # for Pydantic v2


class UserPosition(BaseModel, frozen=True):
    """ 
    user position on market 

    fetch endpoint:
    https://data-api.polymarket.com/positions?sizeThreshold=.1&user={proxy wallet address} 

    attributes:
    
    """
    proxyWallet: str
    asset: str
    conditionId: str
    size: float
    avgPrice: float
    initialValue: float
    currentValue: float
    cashPnl: float
    percentPnl: float
    totalBought: float
    realizedPnl: float
    percentRealizedPnl: float
    curPrice: float
    redeemable: bool
    mergeable: bool
    title: str
    slug: str
    icon: str
    eventSlug: str
    outcome: str
    outcomeIndex: int
    oppositeOutcome: str
    oppositeAsset: str
    endDate: str
    negativeRisk: bool

class Trader(BaseModel, frozen=False):
    proxyWallet: str
    amount: float
    pseudonym: str
    name: str
    bio: str
    profileImage: str
    profileImageOptimized: str

class ActiveTrader(Trader, frozen=False):
    current_value: float
    trades: int

# class Event(BaseModel):
#     id: str = Field(..., description="Event ID")
#     ticker: str = Field(..., description="Ticker symbol")
#     slug: str = Field(..., description="Slug for the event")
#     title: str = Field(..., description="Title of the event")
#     description: str = Field(..., description="Description of the event")

#     resolutionSource: Optional[str] = Field(None, description="Source of the event resolution")
#     startDate: datetime = Field(..., description="Start date of the event")
#     creationDate: datetime = Field(..., description="Creation date of the event")
#     endDate: datetime = Field(..., description="End date of the event")

#     image: Optional[str] = Field(None, description="URL for the event image")
#     icon: Optional[str] = Field(None, description="URL for the event icon")
#     active: bool = Field(True, description="Indicates whether the event is active")
#     closed: bool = Field(False, description="Indicates whether the event is closed")
#     archived: bool = Field(False, description="Indicates whether the event is archived")
#     new: bool = Field(False, description="Indicates whether the event is new")
#     featured: bool = Field(True, description="Indicates whether the event is featured")
#     restricted: bool = Field(True, description="Indicates whether the event is restricted")
#     liquidity: float = Field(..., description="Liquidity of the event", ge=0)
#     volume: float = Field(..., description="Volume of the event", ge=0)
#     openInterest: int = Field(0, description="Open interest in the event")
#     sortBy: str = Field(..., description="Sorting criteria for the event")
#     createdAt: datetime = Field(..., description="Creation date of the event")
#     updatedAt: Optional[datetime] = Field(None, description="Last update date of the event")

#     competitive: float = Field(..., description="Competitive factor for the event", ge=0)
#     volume24hr: float = Field(..., description="Volume over 24 hours for the event", ge=0)
#     volume1wk: float = Field(..., description="Volume over one week for the event", ge=0)
#     volume1mo: float = Field(..., description="Volume over one month for the event", ge=0)
#     volume1yr: float = Field(..., description="Volume over one year for the event", ge=0)
#     enableOrderBook: bool = Field(True, description="Indicates whether to enable order book")
#     liquidityClob: float = Field(..., description="Liquidity CLOB for the event", ge=0)
#     negRisk: bool = Field(True, description="Neg risk indicator for the event")
#     negRiskMarketID: Optional[str] = Field(None, description="Neg risk market ID")
#     commentCount: int = Field(7720, description="Number of comments for the event")
#     cyom: bool = Field(False, description="CYOM flag")
#     showAllOutcomes: bool = Field(False, description="Flag to show all outcomes")
#     showMarketImages: bool = Field(True, description="Flag to show market images")
#     enableNegRisk: bool = Field(True, description="Enable neg risk indicator for the event")
#     automaticallyActive: bool = Field(True, description="Automatically active flag for the event")
#     startTime: Optional[datetime] = Field(None, description="Start time of the event")
#     gmpChartMode: str = Field(..., description="GMP chart mode", ge="")
#     negRiskAugmented: bool = Field(True, description="Neg risk augmented indicator for the event")
#     countryName: str = Field(..., description="Country name for the event")
#     electionType: str = Field(..., description="Election type for the event", ge="")
#     color: Optional[str] = Field(None, description="Color code for the event")

#     featuredOrder: int = Field(2, description="Featured order number for the event")
#     pendingDeployment: bool = Field(False, description="Pending deployment flag for the event")
#     deploying: bool = Field(False, description="Deploying flag for the event")    
