import json
import requests
import discord

client = discord.Client()
TOKEN = "your token here"
baseurl = 'https://data.smartagent.io/v1/jdsports/track-my-order'
colors = {"Payment has been accepted." : 15656761, "Your order is currently being processed." : 15656761, "Your order has been despatched." : 4513044, "Your order has been delivered.": 4513044}

@client.event
async def on_message(message):
    if message.content.startswith("!track"):

        #getting order details from our discord message
        x = message.content.split(" ", 4)
        store, region, postcode, orders = x[1], x[2], x[3], x[4]
        orders = list(orders.split(" "))

        for order in orders:
            try:
                params = {
                    'orderNumber': order,
                    'facia': store + region,
                    'postcode': postcode
                }

                #sending request to order endpoint
                response = requests.get(baseurl, params=params)
                if response.status_code == 200:

                    #parsing response for order info
                    response = json.loads(response.text)
                    orderStatus = response["message"]["text"]
                    fullName = response["addresses"]["delivery"]["firstName"] + " " + response["addresses"]["delivery"]["lastName"]
                    shoeName = response["vendors"][0]["items"][0]["name"]
                    shoeImg = response["vendors"][0]["items"][0]["img"]
                    shoeSize = response["vendors"][0]["items"][0]["size"]

                    #getting corresponding color to status
                    try:
                        embedColor = colors[orderStatus]
                    except:
                        embedColor = 15656761   

                    #sending embed with info
                    embed = discord.Embed(title=shoeName, color=embedColor)
                    embed.set_thumbnail(url=shoeImg)
                    embed.add_field(name="Order", value="||**" + order + "**||", inline=False)
                    embed.add_field(name="Status", value=orderStatus, inline=False)
                    embed.add_field(name="Size", value=shoeSize, inline=True)
                    embed.add_field(name="Name On Order", value=fullName, inline=True)
                    embed.set_footer(text="Mesh Order Tracker By Eddie#3333")
                    await message.channel.send(embed=embed)
                
                else:
                    response = json.loads(response.text)
                    await message.channel.send("Error Tracking Order: " + response["message"])


            except Exception as e:
                print(e)
                message.channel.send("Error Tracking Order")



@client.event
async def on_ready():
    print("Mesh order tracker made by @eddie#3333. Bot is ready.")

if __name__ == "__main__":
    client.run(TOKEN)
