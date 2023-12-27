from messages.customer import SearchResult
from messages.store import Search, PlaceOrder
from uagents import Agent, Context
from .store import agent as storeAgent

agent = Agent(name='customer')


@agent.on_interval(1)
async def send_search_query(ctx: Context):

    item_name = input('what are you looking for...:  ')

    min_item_price = input('whats is min price of item')

    min_item_price = float(min_item_price) if(min_item_price)  else float(0)

    max_item_price = input('what is the max price of item')
    
    max_item_price = float(max_item_price) if(max_item_price)  else float(0)

    if item_name != '':
        await ctx.send(storeAgent.address, Search(item_name=item_name, max_price=max_item_price, min_price=min_item_price))



@agent.on_message(model=SearchResult)
async def handel_result(ctx, sender, result):
    data = result.result[0]
    count = 1
    ctx.logger.info("So we have: ")
    new_data = []
    for item in data:
        ctx.logger.info(f"{count} {item} price {data[item]['price']}")
        count += 1
        new_data.append(item)
    ctx.logger.info("Check for avalibility status... ")
    
    number = int(input("give the product id number to check avalibility: "))

    number = number - 1

    if not(len(data) > number):
        ctx.logger.info('Invlalid Choice')
    else:
        if data[new_data[number]]['availability']:
            ctx.logger.info('Product is avaliable')

            # ctx.logger.info('Do you want to place order')

            order = input('Do you want to place order')
            if order or order.lower() == 'yes':
                
                await ctx.send(sender, PlaceOrder(item={new_data[number]: data[new_data[number]]}))
                

            else:
                ctx.logger.info('Ohk thanks for using')

        else:
            ctx.logger.info('Product is not avaliable')

