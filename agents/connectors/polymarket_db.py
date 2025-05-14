import sqlite3

from sqlite3 import Connection
from logger import logging

from agents.utils.objects import Trade, ActivityUser, UserPosition, TradedUser, ValueUser
import agents.utils.consts as consts


class PolymarketDb():
    def __init__(self):
        self.connection = self._init_create_database()
        self.cursor = self.connection.cursor()

    
    def create_db_tables(self) -> None:
        # create sql tables
                self._init_trade()
                self._init_polymarket_event()
                self._init_activity_user()
                self._init_value_user()
                self._init_user_position()

    def _init_create_database(self) -> Connection:
        logging.info(f"create sqlite3 database: \'{consts._DB_NAME}\'")
        return sqlite3.connect(consts._DB_NAME)
        
    def _init_trade(self) -> None:
        logging.info(f"create sql table: \'{consts._TRADE}\'")
        self.cursor.execute(consts.CREATE_TABLE_TRADE)

    def _init_polymarket_event(self) -> None:
        logging.info(f"create sql table: \'{consts._POLYMARKET_EVENT}\'")
        self.cursor.execute(consts.CREATE_TABLE_POLYMARKET_EVENT)

    def _init_market(self) -> None:
        _TABLE_NAME = "market"
        logging.info(f"create sql table: \'{_TABLE_NAME}\'")
        self.cursor.execute(consts.CREATE_TABLE_MARKET)

    def _init_activity_user(self):
        _TABLE_NAME = "activity_user" 
        logging.info(f"create sql table: \'{consts._ACTIVITY_USER}\'")
        self.cursor.execute(consts.CREATE_TABLE_ACTIVITY_USER)

    def _init_value_user(self) -> None:
        _TABLE_NAME = "value_user"
        logging.info(f"create sql table: \'{consts._VALUE_USER}\'")
        self.cursor.execute(consts.CREATE_TABLE_VALUE_USER)

    def _init_traded_user(self) -> None:
        _TABLE_NAME = "traded_user"
        logging.info(f"create sql table: \'{consts._TRADED_USER}\'")
        self.cursor.execute(consts.CREATE_TABLE_TRADED_USER)

    def _init_user_position(self) -> None:
        _TABLE_NAME = "user_position"
        logging.info(f"create sql table \'{consts._USER_POSITION}\'")
        self.cursor.execute(consts.CREATE_TABLE_USER_POSITION)

    def close(self) -> None:
        self.connection.close()

    def write_trade(self, trade: Trade) -> None:
        self.cursor.execute(consts.INSERT_TRADE_TABLE, (
            trade['id'],
            trade['taker_order_id'],
            trade['market'],
            trade['asset_id'],
            trade['side'],
            trade['size'],
            trade['fee_rate_bps'],
            trade['price'],
            trade['status'],
            trade['match_time'],
            trade['last_update'],
            trade['outcome'],
            trade['maker_address'],
            trade['owner'],
            trade['transaction_hash'],
            trade['bucket_index'],
            trade['maker_orders'],
            trade['type']
        ))
        self.connection.commit()
        
    
    def read_trade(self) -> list[Trade]:
        self.cursor.execute(f"SELECT * FROM {consts._TRADE}")
        rows = self.cursor.fetchall()
        return rows

    def write_activity_user(self, activity_user: ActivityUser) -> None:
        if activity_user is None:
            # Handle the case where activity_user is None
            raise ValueError("activity_user cannot be None")
    
        try:
            logging.info(f"writing 0x{activity_user.__hash__()} to sqlite3 database: {consts._DB_NAME}")
            self.cursor.execute(consts.INSERT_ACTIVITY_USER_TABLE, (
                activity_user.proxyWallet,
                activity_user.timestamp,
                activity_user.conditionId,
                activity_user.type,
                activity_user.size,
                activity_user.usdcSize,
                activity_user.transactionHash,
                activity_user.price,
                activity_user.asset,
                activity_user.side,
                activity_user.outcomeIndex,
                activity_user.title,
                activity_user.slug,
                activity_user.icon,
                activity_user.eventSlug,
                activity_user.outcome,
                activity_user.name,
                activity_user.pseudonym,
                activity_user.bio,
                activity_user.profileImage,
                activity_user.profileImageOptimized
            ))
            self.connection.commit()
        except Exception as e:
            logging.exception("SqliteException")


    def read_activity_user(self) -> list[ActivityUser]:
        self.cursor.execute(f"SELECT * FROM {consts._ACTIVITY_USER}")
        rows = self.cursor.fetchall()
        return rows

    def write_user_position(self, user_position: UserPosition) -> None:
        if user_position is None:
            raise ValueError(f"user_position cannot be None")
        
        try:
            logging.info(f"writing 0x{user_position.__hash__()} to sqlite3 database {consts._DB_NAME}")
            self.cursor.execute(consts.INSERT_USER_POSITION_TABLE, (
                user_position.proxyWallet,
                user_position.asset,
                user_position.conditionId,
                user_position.size,
                user_position.avgPrice,
                user_position.initialValue,
                user_position.currentValue,
                user_position.cashPnl,
                user_position.percentPnl,
                user_position.totalBought,
                user_position.realizedPnl,
                user_position.percentRealizedPnl,
                user_position.curPrice,
                user_position.redeemable,
                user_position.mergeable,
                user_position.title,
                user_position.slug,
                user_position.icon,
                user_position.eventSlug,
                user_position.outcome,
                user_position.outcomeIndex,
                user_position.oppositeOutcome,
                user_position.oppositeAsset,
                user_position.endDate,
                user_position.negativeRisk
            ))
            self.connection.commit()
        except Exception as e:
            logging.exception("SqliteException")

    def write_traded_user(self, traded_user: TradedUser) -> None:
        if traded_user is None:
            raise ValueError(f"traded_user cannot be None")
        
        try: 
            logging.info(f"writing {traded_user.__hash__()} to sqlite3 database {consts._DB_NAME}")
            self.cursor.execute(consts.INSERT_TRADED_USER_TABLE, (
                traded_user.user,
                traded_user.traded
            ))
            self.connection.commit()
        except Exception as e:
            logging.exception("SqliteException")

    def write_value_user(self, value_user: ValueUser) -> None:
        if value_user is None:
            raise ValueError(f"value_user cannot be none")
        
        try:
            logging.info(f"writing {value_user.__hash__()} to sqlite3 database {consts._DB_NAME}")
            self.cursor.excute(consts.INSERT_VALUE_USER_TABLE, (
                value_user.user,
                value_user.value
            ))
        except Exception as e:
            logging.exception("SqliteException")

    
    def read_activity_positions_by_user_timestamp(self, timestamp: int) -> list[ActivityUser]:
        obj = []
        self.cursor.execute(
            f"""
                SELECT proxy_wallet, timestamp, conditionId, type, size, usdcSize, transactionHash,
                  price, asset, side, outcomeIndex, title, slug, icon, event_slug, outcome,
                  name, pseudonym, bio, profile_image, profile_image_optimized
                FROM activity_user 
                -- INNER JOIN user_position 
                -- ON activity_user.asset = user_position.asset 
                WHERE activity_user.side = 'BUY' 
                AND activity_user.timestamp > 1747062974 -- {timestamp} 
                GROUP BY conditionId
                ORDER BY activity_user.timestamp desc;
            """   
        )
        
        # rows = self.cursor.fetchall()
        for r in self.cursor.fetchall():
            _activity_user = ActivityUser(
                proxyWallet=r[0], 
                timestamp=r[1], 
                conditionId=r[2], 
                type=r[3], 
                size=r[4], 
                usdcSize=r[5], 
                transactionHash=r[6], 
                price=r[7], 
                asset=r[8], 
                side=r[9], 
                outcomeIndex=r[10], 
                title=r[11], 
                slug=r[12], 
                icon=r[13], 
                eventSlug=r[14], 
                outcome=r[15], 
                name=r[16], 
                pseudonym=r[17], 
                bio=r[18], 
                profileImage=r[19], 
                profileImageOptimized=r[20]
            )
            # _activity_user = ActivityUser(**dict(row))
            obj.append(_activity_user)

        # ActivityUser.model_validate(dict(row)) for row in rows
        return obj
    
    
    
