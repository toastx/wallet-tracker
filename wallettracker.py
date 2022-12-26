import schedule
from time import sleep
from requests import request
import lightbulb
import hikari
import logging
from lightbulb.ext import tasks
import datetime
import string
from discord_keys import wt_wallettracker

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("requests.packages.urllib3").setLevel(logging.CRITICAL)

token = wt_wallettracker
bot = lightbulb.BotApp(token=token)
channel_id = 1017070434707058709
times= datetime.datetime.now()
times = times.strftime("%D")
footer = f"Made with ❤️ by toastx#9006  •  {times}"
tasks.load(bot)


buffer_lst = ["yo"]
wallet_address="{any wallet address}"

@tasks.task(s=10, auto_start=True)
async def tracker():
    url = f"http://api-mainnet.magiceden.dev/v2/wallets/{wallet_address}/activities?offset=0&limit=1"
    payload = {}
    headers = {}
    response = request("GET", url, headers=headers, data=payload)
    data = response.json()
    if buffer_lst:
            if data[0] != buffer_lst[0]:
                        buffer_lst.pop()
                        buffer_lst.append(data[0])
                        sleep(1)
                        action = str(buffer_lst[0]["type"]).capitalize()
                        collectionSymbol = str(buffer_lst[0]["collectionSymbol"])
                        price = str(buffer_lst[0]["price"]).capitalize()
                        tokenMint = str(buffer_lst[0]["tokenMint"])
                        url2 = f"http://api-mainnet.magiceden.dev/v2/tokens/{tokenMint}"
                        response2 = request("GET", url2)
                        data2 = response2.json()
                        name = data2["name"]
                        image = data2["image"]
                        url3= f"http://api-mainnet.magiceden.dev/v2/collections/{collectionSymbol}"
                        response3 = request("GET", url3)
                        data3 = response3.json()
                        fp = data3['floorPrice']
                        title = f'{person-to-track}{action}ed {name}'
                        description = f"**Price** \u3000\u3000\u3000 **Floor Price** \n {price} ◎ \u3000 \u3000 {(fp/1000000000)}◎"
                        color = "#9f40ff"
                        if "buyNow" in data[0]['type']:
                            if data[0]["buyer"]== wallet_address:
                                title =f"{person-to-track} bought {name}"
                                color ="#66FF00"
                            elif data[0]["seller"]== wallet_address:
                                title =f"{person-to-track} sold {name}"
                                color ="#FF0000"
                        embed = hikari.Embed(title=title,
                                             url=f"https://magiceden.io/item-details/{tokenMint}",
                                                 description=description,
                                                 color=color)
                        embed.set_footer(footer)
                        embed.set_thumbnail(image)
                        await bot.rest.create_message(channel_id, embed=embed)
                        sleep(1)

bot.run()


