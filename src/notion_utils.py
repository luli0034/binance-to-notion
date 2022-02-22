class NotionDatabase:
    title = [{"type": "text", "text": {"content": 'Crypto Assets'}}]
    icon = {"type": "emoji", "emoji": "💸"}
    properties = {
        "Tags":None,
        "Name": {
            "title": {}
        },
        "2. Profit": {
            "number": {}
        },
        "3. Total Qty": {
            "number": {}
        },
        "4. Avg. Buying Price": {
            "number": {}
        },
        "5. Price": {
            "number": {}
        },
        "6. Latest Update ID": {
            "number": {}
        }
        
    }

    
def get_notion_row(name, profit, qty, avgPrice, price, latest_update):
    row = {
        "Name": {"title": [{"text": {"content": name}}]},
        "2. Profit":  {
            "id": f"{name}_profit",
            "type": "number",
            "number": profit
        },
        "3. Total Qty":  {
            "id": f"{name}_qty",
            "type": "number",
            "number": qty
        },
        '4. Avg. Buying Price':  {
            "id": f"{name}_avgPrice",
            "type": "number",
            "number": avgPrice
        },
        '5. Price': {
            "id": f"{name}_price",
            "type": "number",
            "number": price
        },
        '6. Latest Update ID':{
            "id": f"{name}_latest_update",
            "type": "number",
            "number": latest_update
        }

    }

    return row

def get_plain_text_from_properities(properities, col):
    try:
        return properities[col]['rich_text'][0]['plain_text']
    except Exception as e:
        return None
    