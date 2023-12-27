from uagents import Bureau
from agents import store, customer


server = Bureau()

server.add(customer.agent)
server.add(store.agent)

server.run()