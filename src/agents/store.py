from messages.store import Search, PlaceOrder
from messages.customer import SearchResult
from uagents import Agent, Context


agent = Agent(name='store')

product_data = {
    'laptops': {
        'Laptop1': {'price': 1000, 'availability': True},
        'Laptop2': {'price': 1200, 'availability': False},
        'Laptop3': {'price': 800, 'availability': True}
    },
    
    'tv': {
        'TV1': {'price': 500, 'availability': True},
        'TV2': {'price': 700, 'availability': True},
        'TV3': {'price': 1000, 'availability': False}
    },
    
    'smartphones': {
        'Phone1': {'price': 300, 'availability': True},
        'Phone2': {'price': 400, 'availability': True},
        'Phone3': {'price': 600, 'availability': False}
    },
    
    'watches': {
        'Watch1': {'price': 100, 'availability': True},
        'Watch2': {'price': 150, 'availability': False},
        'Watch3': {'price': 120, 'availability': True}
    }
}

@agent.on_message(model=Search)
async def handel_search(ctx: Context, sender: str, msg: Search):
    data = []
    for i in product_data:
        if msg.item_name in i.lower() or i.lower() in msg.item_name:
            
            if msg.max_price == msg.min_price:
                data.append(product_data[i])

            else:
                new_data = {}
                for k in product_data[i]:
                    if msg.max_price >= product_data[i][k]['price'] and msg.min_price <= product_data[i][k]['price']:
                        new_data[k] = product_data[i][k]

                data.append(new_data)
                
    if data:
        await ctx.send(sender, SearchResult(result=data))
    else:
        ctx.logger.info(f'We dont sell this type of product')


@agent.on_message(model=PlaceOrder)
async def place_order(ctx, sender, msg):
    data = msg.item
    for i in data:
        ctx.logger.info(f"You have ordered {i} of cost {data[i]['price']}")

    ctx.logger.info("Order Placed Successfully\n\n\n\n\n")
    


