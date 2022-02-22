<div align="center">
	<h1><img src="https://assets.trustwalletapp.com/blockchains/binance/info/logo.png" width="50" height="50"> Show My Binance Wallet on Notion <img src="https://upload.wikimedia.org/wikipedia/commons/4/45/Notion_app_logo.png?20200221181224" width="50" height="50"></h1>
	<p>
		<b>Show me the money!!!</b>
	</p>
	<br>
</div>

In order to inspect the detail of Crypto Investment by each symbol such as ***averaging buying price of*** `BTC/USDT`. I simply integrate **[Binance API](https://binance-docs.github.io/apidocs/spot/en/#introduction)** and **[Notion integrations](https://developers.notion.com/)** in this project.

# 📽️ Quick Demo

# 📃 Requirements

## Binance API Setup

- Create Binance API Key step by step by following the tutorial.
    
    [https://www.binance.com/en/support/faq/360002502072](https://www.binance.com/en/support/faq/360002502072)
    
- ✨ Copy the **API Key** (`API_KEY`)
- ✨ Copy the **Secret Key** (`SECRET_KEY`)

## **Notion Integration Setup**

1. Open the workspace setting by clicking on the `Settings and Members` option on the left navigation bar. And click on the button to go manage the notion integrations.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/9011e1b3-3964-465e-8b13-5dafda34dff1/Untitled.png)
    
2. Create a new integration with authentication of Read, Update and Insert Content.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1649b369-9cdb-491b-ae66-9288330e9c9e/Untitled.png)

1. Once you save your changes, you will see the integration token. Keep it for further use.
    
    ✨Keep the **Internal Integration Token (**`NOTION_AUTH`**)**.
    

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/33d6d54e-9524-4c06-9a5b-65a58706e6a0/Untitled.png)

## Database Setup

1. (Important!!) Create a new page under your **WORKSPACE** instead of **PRIVATE** page.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/08a98d31-ee1c-4ada-8004-12102397071d/Untitled.png)

1. Share the access to Integration we just created.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/c751af53-4234-4d4a-81e8-00412d61a2a1/Untitled.png)

1. Type `/database` and choose `Table database - Inline` in anywhere. Then copy its link to get the `database_id` for further use.
    
    ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/3d7bf2b8-19f5-4bdf-b6f8-9a8adc14fc21/Untitled.png)
    
    The format of copied link will like below: 
    
    `https://www.notion.so/{WORKSPACE}/{DATABASE_ID}?v={SOME_ID}`
    
    ✨ Keep the part of `{DATABASE_ID}` (`database_id`).
    

# 🚀 Usage

Steps to build a Docker image:

1. ***Clone this repo***
    
    ```bash
    git clone https://github.com/luli0034/binance-to-notion.git
    ```
    
2. ***Build the image***
    
    ```bash
    cd ./binance-to-notion
    docker build -t binance2notion . --no-cache
    ```
    
3. ***Set container parameters***
    
    Before running the built image, we need to set the environment variables for Binance API Key and secret as well as notion authentication.
    
    - `API_KEY` → Binance API key. Create by [Binance API Setup**](##**Binance API Setup**)**
    - `SECRET_KEY`→ Binance secret key. Create by [Binance API Setup**](##**Binance API Setup**)**
    - `NOTION_AUTH` → Notion developer authentication key. Create by [Notion Integration Setup**](##**Notion Integration Setup**)**
4. **Run the image's default command with the required parameters.**
    - `db_id` → Database ID ****which you want to update. Create by [Database Setup](##Database Setup)
    - `base` → Coinbase (e.g. USDT, BUSD).
    
    ```docker
    docker run --env API_KEY={API_KEY}\
               --env SECRET_KEY={SECRET_KEY}\
               --env NOTION_AUTH={NOTION_AUTH}\
               binance2notion --db_id={database_id} --base={coinbase}
    ```
