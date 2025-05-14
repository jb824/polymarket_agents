_DB_NAME = "polymarket.db"

_TRADE = "trade"
_POLYMARKET_EVENT = "polymarket_event"
_MARKET = "market"
_ACTIVITY_USER = "activity_user"
_VALUE_USER = "value_user"
_TRADED_USER = "traded_user"
_USER_POSITION = "user_position"

CREATE_TABLE_TRADE = f'''
    CREATE TABLE IF NOT EXISTS {_TRADE} (
        id INTEGER PRIMARY KEY,
        taker_order_id TEXT NOT NULL,
        market TEXT NOT NULL,
        asset_id TEXT NOT NULL,
        side TEXT NOT NULL,
        size REAL NOT NULL,  -- converted to real since it's a size value
        fee_rate_bps TEXT NOT NULL,
        price REAL NOT NULL,  -- converted to real since it's a price value
        status TEXT NOT NULL,
        match_time DATE NOT NULL,
        last_update DATE NOT NULL,
        outcome TEXT NOT NULL,
        maker_address TEXT NOT NULL,
        owner TEXT NOT NULL,
        transaction_hash TEXT NOT NULL,
        bucket_index TEXT NOT NULL,
        maker_orders TEXT,  -- stored as a comma-separated list
        type TEXT NOT NULL,
        FOREIGN KEY (market) REFERENCES Markets (slug)
    );
'''

CREATE_TABLE_POLYMARKET_EVENT = f'''
    CREATE TABLE IF NOT EXISTS {_POLYMARKET_EVENT} (
        id TEXT NOT NULL,
        ticker TEXT,
        slug TEXT,
        title TEXT,
        start_date INTEGER,
        created_at INTEGER,
        end_date INTEGER,
        image TEXT,
        icon TEXT,
        active INTEGER,
        closed INTEGER,
        archived INTEGER,
        new INTEGER,
        featured INTEGER,
        restricted INTEGER,
        liquidity REAL,
        volume REAL,
        review_status TEXT,
        created_at_date INTEGER,
        updated_at_date INTEGER,
        competitive REAL,
        volume_24hr REAL,
        enable_order_book INTEGER,
        liquidity_clob REAL,
        sync INTEGER,
        comment_count INTEGER,
        markets TEXT,
        tags TEXT,
        cyom INTEGER,
        show_all_outcomes INTEGER,
        show_market_images INTEGER
    );
'''

CREATE_TABLE_MARKET = f'''
    CREATE TABLE IF NOT EXISTS {_MARKET} (
        id INTEGER PRIMARY KEY,
        question TEXT,
        condition_id TEXT,
        slug TEXT,
        resolution_source TEXT,
        end_date INTEGER,
        liquidity REAL,
        start_date INTEGER,
        image TEXT,
        icon TEXT,
        description TEXT,
        outcome TEXT,
        outcome_prices TEXT,
        volume REAL,
        active INTEGER, -- boolean value
        closed INTEGER, -- boolean value
        market_maker_address TEXT,
        created_at INTEGER,
        updated_at INTEGER,
        new INTEGER, -- boolean value
        featured INTEGER, -- boolean value
        submitted_by TEXT,
        archived INTEGER, -- boolean value
        resolved_by TEXT,
        restricted INTEGER, -- boolean value
        group_item_title TEXT,
        group_item_threshold INTEGER,
        question_id TEXT,
        enable_order_book INTEGER, -- boolean value
        order_price_min_tick_size REAL,
        order_min_size INTEGER,
        volume_num REAL,
        liquidity_num REAL,
        end_date_iso INTEGER,
        start_date_iso INTEGER,
        has_reviewed_dates INTEGER, -- boolean value
        volume_24hr REAL,
        clob_token_ids TEXT,
        uma_bond INTEGER,
        uma_reward INTEGER,
        volume_24hr_clob REAL,
        volume_clob REAL,
        liquidity_clob REAL,
        accepting_orders INTEGER, -- boolean value
        neg_risk INTEGER, -- boolean value
        comment_count INTEGER,
        sync INTEGER, -- boolean value
        events TEXT,  -- stored as JSON
        ready INTEGER, -- boolean value
        deployed INTEGER, -- boolean value
        funded INTEGER, -- boolean value
        deployed_timestamp INTEGER,
        accepting_orders_timestamp INTEGER,
        cyom INTEGER, -- boolean value
        competitive REAL,
        pager_duty_notification_enabled INTEGER, -- boolean value
        review_status TEXT,
        approved INTEGER, -- boolean value
        clob_rewards TEXT,  -- stored as JSON
        rewards_min_size INTEGER,
        rewards_max_spread REAL,
        spread REAL
    );
'''

CREATE_TABLE_ACTIVITY_USER = f'''
    CREATE TABLE IF NOT EXISTS {_ACTIVITY_USER} 
    (
        id INTEGER PRIMARY KEY,
        proxy_wallet TEXT CHECK (length(proxy_wallet) <= 200),
        timestamp INTEGER,
        conditionId TEXT CHECK (length(conditionId) <= 200),
        type TEXT,
        size REAL,
        usdcSize REAL,
        transactionHash TEXT CHECK (length(transactionHash) <= 200),
        price REAL,
        asset TEXT CHECK (length(asset) <= 200),
        side TEXT,
        outcomeIndex INTEGER,
        title TEXT CHECK (length(title) <= 500),
        slug TEXT,
        icon TEXT CHECK (length(icon) <= 500),
        event_slug TEXT CHECK (length(event_slug) <= 500),
        outcome TEXT,
        name TEXT,
        pseudonym TEXT,
        bio TEXT,
        profile_image TEXT CHECK (length(profile_image) <= 200),
        profile_image_optimized TEXT CHECK (length(profile_image_optimized) <= 200)            
    );           
'''

CREATE_TABLE_VALUE_USER = f'''
    create table IF NOT EXISTS {_VALUE_USER} (
        id INTEGER PRIMARY KEY,
        user TEXT,
        value REAL
    );      
'''

CREATE_TABLE_TRADED_USER = f'''
    CREATE TABLE IF NOT EXISTS {_TRADED_USER} (
        id INTEGER PRIMARY KEY,
        user TEXT,
        traded INTEGER
    );
'''

CREATE_TABLE_USER_POSITION = f'''
    CREATE TABLE IF NOT EXISTS {_USER_POSITION} (
        id INTEGER PRIMARY KEY,
        proxyWallet TEXT NOT NULL,
        asset TEXT NOT NULL,
        conditionId TEXT NOT NULL,
        size REAL NOT NULL,
        avgPrice REAL NOT NULL,
        initialValue REAL NOT NULL,
        currentValue REAL NOT NULL,
        cashPnl REAL NOT NULL,
        percentPnl REAL NOT NULL,
        totalBought REAL NOT NULL,
        realizedPnl REAL NOT NULL,
        percentRealizedPnl REAL NOT NULL,
        curPrice REAL NOT NULL,
        redeemable INTEGER NOT NULL,  -- converted to integer since it's a boolean
        mergeable INTEGER NOT NULL,  -- converted to integer since it's a boolean
        title TEXT NOT NULL,
        slug TEXT NOT NULL,
        icon TEXT NOT NULL,
        eventSlug TEXT NOT NULL,
        outcome TEXT NOT NULL,
        outcomeIndex INTEGER NOT NULL,  -- converted to integer since it's an integer
        oppositeOutcome TEXT NOT NULL,
        oppositeAsset TEXT NOT NULL,
        endDate INTEGER NOT NULL,
        negativeRisk INTEGER NOT NULL  -- converted to integer since it's a boolean
    );
'''

INSERT_TRADE_TABLE = f"""
    INSERT INTO {_TRADE} (
        id, taker_order_id, market, asset_id, side, size, fee_rate_bps, price, status,
        match_time, last_update, outcome, maker_address, owner, transaction_hash,
        bucket_index, maker_orders, type
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_ACTIVITY_USER_TABLE = f"""
    INSERT INTO {_ACTIVITY_USER} (
        proxy_wallet, 
        timestamp, 
        conditionId, 
        type, 
        size, 
        usdcSize, 
        transactionHash, 
        price, 
        asset, 
        side, 
        outcomeIndex, 
        title, 
        slug, 
        icon, 
        event_slug, 
        outcome, 
        name, 
        pseudonym, 
        bio, 
        profile_image, 
        profile_image_optimized
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);    
"""

INSERT_USER_POSITION_TABLE = f"""
    INSERT INTO {_USER_POSITION} (
        proxyWallet, 
        asset, 
        conditionId, 
        size, 
        avgPrice, 
        initialValue, 
        currentValue, 
        cashPnl, 
        percentPnl, 
        totalBought, 
        realizedPnl, 
        percentRealizedPnl, 
        curPrice, 
        redeemable, 
        mergeable, 
        title, 
        slug, 
        icon, 
        eventSlug, 
        outcome, 
        outcomeIndex, 
        oppositeOutcome, 
        oppositeAsset, 
        endDate, 
        negativeRisk
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

INSERT_TRADED_USER_TABLE = f"""
    INSERT INTO {_TRADED_USER} (
        user,
        traded
    ) values (?, ?)
"""

INSERT_VALUE_USER_TABLE = f"""
    INSERT INTO {_VALUE_USER} (
        user, 
        value
    ) values (?, ?)
"""