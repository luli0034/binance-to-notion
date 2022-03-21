from get_logger import get_logger
from utils import retry
from notion_fun import query_asset_by_crypto_name
from notion_utils import get_notion_row
logger = get_logger(__name__)
class Coin:

    def __init__(self, binance, name, pairwith):
        self.symbol = name + pairwith
        self.binance = binance
        self.name = name
        self.fromId, self.page_id = None, None        

    def set_basic_info(self, asset_info={}):
        try:
            self.curCost = float(asset_info["qty"]*asset_info["avgPrice"])
            self.curQty = float(asset_info['qty'])
            self.fromId = asset_info["fromId"]
            self.page_id = asset_info["page_id"]
        except KeyError:
            logger.debug(f'There is no asset for {self.symbol} in the current account')
            self.curCost = 0
            self.curQty = 0
        
        OrderQty, OrderCost = self._get_asset_from_order_history()
        self.curQty += OrderQty
        self.curCost += OrderCost
        self.curAvgBuyPrice = self.curCost / self.curQty
        self.acctProfit = self._get_acct_profit()

    def output_notion_row(self):
        try:
            return self.page_id, get_notion_row(
                                    name=self.name,
                                    profit=self.acctProfit, 
                                    qty=self.curQty, 
                                    avgPrice=self.curAvgBuyPrice, 
                                    price=self.price, 
                                    latest_update=self.fromId
                                )
        except Exception as e:
            logger.warning(f"Output row after running set_basic_info(). {e}")
            return

    @retry(logger=logger)
    def _get_acct_profit(self):
        try:
            logger.info(f'Fetch the latest price of {self.symbol}.')
            self.price=float(self.binance.get_symbol_ticker(symbol=self.symbol)['price'])
            return self.price * self.curQty - self.curCost
        except Exception as e:
            logger.error(f"Can't fetch the latest price of {self.symbol}, {e}")
            raise
        
    @retry(logger=logger)
    def _get_asset_from_order_history(self):
        order_history = self._get_order_history()
        qty, cost = 0.0, 0.0
        if len(order_history) < 1:
            return qty, cost
        self.fromId = order_history[-1]['id']
        
        for order in order_history:
            if order['isBuyer']:
                qty += float(order['qty']) - float(order['commission'])
                cost += float(order['price']) * float(order['qty'])
            elif not order['isBuyer']:
                qty -= float(order['qty'])
                cost -= float(order['price']) * float(order['qty'])
        
        return qty, cost

    @retry(logger=logger)
    def _get_order_history(self):
        try:
            if self.fromId:
                logger.info(f'Fetch the historical trades of {self.symbol}, start from transaction ID of {self.fromId}.')
                order_history = self.binance.get_my_trades(symbol=self.symbol, fromId=self.fromId+1, limit=1000)
            else:
                logger.info(f'Fetch the historical trades of {self.symbol}.')
                order_history = self.binance.get_my_trades(symbol=self.symbol)
            return order_history 
        except Exception as e:
            logger.error(f"Can't fetch the trades of {self.symbol}, {e}")
            raise



class Account():

    def __init__(self, binance, pairwith):
        self.binance = binance
        self.pairwith = pairwith
        self.notion = None
        
    
    def init_notion_database(self, notion, database_id):
        self.notion = notion
        self.database_id = database_id

    def init_account_assert(self):
        try:
            logger.info("Fetch the account info.")
            acct_bal = self.binance.get_account()['balances']
        except Exception as e:
            logger.error("Error, can't get account info.")
            raise

        self.acctBalances = [bal['asset'] for bal in acct_bal if float(bal['free'])>0]
        self.acctAsset = {}
        for coin in self.acctBalances:
            if coin != self.pairwith:
                try:
                    self.binance.get_my_trades(symbol=coin+self.pairwith)
                except:
                    continue
                self.acctAsset[coin] = Coin(self.binance, coin, self.pairwith)
                if self.notion is not None:
                    logger.info(f"Query {coin} asset from database")
                    # Query page by crypto name
                    asset_info = query_asset_by_crypto_name(self.notion,self.database_id, coin)
                    self.acctAsset[coin].set_basic_info(asset_info)
                else:
                    logger.error("Please init_notion_database first")
                    raise ValueError
                

    
    
        