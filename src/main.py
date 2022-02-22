import os 
import argparse
import json
import time
from binance.client import Client as BinanceClient
from binance_fun import Account
from notion_fun import get_notion_conn
from notion_fun import *
from utils import retry




def run():
    parser = argparse.ArgumentParser(description='Data processing')
    parser.add_argument("--db_id", help="database id in notion", required=True)
    parser.add_argument("--base", help="coin which you use it to buy", required=True)

    args = parser.parse_args()
    notion = get_notion_conn(auth=os.environ['NOTION_AUTH'])

    is_new_table = len(notion.databases.query(database_id=args.db_id)['results'][0]['properties'])!=6

    if is_new_table:
        # Create a empty database and initial its format
        init_database_with_specify_format(notion, args.db_id)           
        # Empty pages under the init database
        empty_database_with_database_id(notion, args.db_id)

    binance = BinanceClient(os.environ["API_KEY"], os.environ["SECRET_KEY"])    
    account = Account(binance, args.base)
    account.init_notion_database(notion, args.db_id)
    account.init_account_assert()

    for key, coin in account.acctAsset.items():
        page_id, new_page = coin.output_notion_row()
        if page_id is None:
            # Insert a new page into database
            code = insert_new_page(notion, args.db_id, new_page)
            logger.info(f"Create assets successfully ({args.base})")
        else:
            # Upadate page with updated page
            code = update_page(notion, page_id, new_page)
            logger.info(f"Update assets successfully ({args.base})")
        

    

    
if __name__ == '__main__':
    run()