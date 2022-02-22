import os
from notion_client import Client
from notion_utils import NotionDatabase, get_notion_row
from get_logger import get_logger

logger = get_logger(__name__)
def get_notion_conn(auth):
    try:
        conn = Client(auth=auth)
        return conn
    except:
        logger.error(f"""Couldn't connect to notion with secret {auth}. \n
                         Please check your authentication number is correct.
                      """)
        raise
    

def query_asset_by_crypto_name(notion, database_id, name):
    try:
        results = notion.databases.query(database_id=database_id, filter={"and":[{"property":"Name", "text":{"equals":name}}]})['results']
        if results:
            logger.info(f"There is an exist record of {name} in database, update the current asset.")
            if len(results) > 0: logger.warning(f"Exist more than 1 records of {name}, use the first one.")
            properties = results[0].get("properties")
            page_id = results[0].get("id")
            asset_info = {
                'page_id': page_id,
                'name': name,
                'price': properties.get("5. Price").get("number"),
                'profit': properties.get("2. Profit").get("number"),
                'qty': properties.get("3. Total Qty").get("number"),
                'avgPrice': properties.get("4. Avg. Buying Price").get("number"),
                'fromId': properties.get('6. Latest Update ID').get("number")
            }
            return asset_info
        
        else:
            logger.info(f"There is no any record of {name} in database, add a new one.")
            return {}
    except Exception as e:
        logger.error(f"{e}")
        raise


def init_database_with_specify_format(notion, database_id):
    try:
        logger.info("Initializing database with specify format")
        code = notion.databases.update(
                database_id=database_id,
                properties=NotionDatabase.properties,
                title=NotionDatabase.title,
                icon=NotionDatabase.icon
            )
    except Exception as e:
        logger.error(f"Initialize database {database_id} error, {e}")
        raise

    return code

def empty_database_with_database_id(notion, database_id):
    try:
        logger.debug(f"Empty database records.")
        results = notion.databases.query(database_id=database_id)['results']
        if results:
            for result in results:
                page_id = result.get("id")
                try:
                    notion.pages.update(page_id=page_id, archived=True)
                except Exception as e:
                    logger.error(f"Error when processing page: {page_id}, {e}")
                    raise

    except Exception as e:
            logger.error(f"Empty database {database_id} error, {e}")
            raise


def insert_new_page(notion, database_id, new_page):
    try:
        response = notion.pages.create(
            parent={"database_id": database_id},
            properties=new_page
        )
    
        return response
    except Exception as e:
        logger.error(f"Error when insert page into {database_id}, {e}")
        raise

def update_page(notion, page_id, new_page):
    try:
        response = notion.pages.update(
            page_id=page_id,
            properties=new_page
        )
    
        return response
    except Exception as e:
        logger.error(f"Error when update page {page_id}, {e}")
        raise

# def run():
   
    # Create a empty database and initial its format
    # code = init_database_with_specify_format(notion, new_db_id)
    
    ## Empty pages under the init database
    # code = empty_database_with_database_id(notion, new_db_id)

    ## Insert a new page into database
    # code = insert_new_page(notion, new_db_id, new_row)

    # # Query page by crypto name
    # asset_info = query_asset_by_crypto_name(notion, new_db_id, 'BTC')
    
    # # Update new values
    # updated_row = get_row(
    #     name=asset_info["name"] ,
    #     profit=asset_info["profit"]+1, 
    #     qty=asset_info["qty"]+10, 
    #     avgPrice=asset_info["avgPrice"]+3, 
    #     price=asset_info["price"]+4, 
    #     latest_update=asset_info["fromId"]+"newnew"
    # )

    ## Upadate page with updated page
    # code = update_page(notion, asset_info["page_id"], updated_row)
  
# if __name__ == '__main__':
#     run()