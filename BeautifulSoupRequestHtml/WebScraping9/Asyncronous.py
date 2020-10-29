import time
from requests_html import AsyncHTMLSession

assession = AsyncHTMLSession()

async def get_delay1():

    r = await assession.get('https://httpbin.org/delay/1')
    return r

async def get_delay2():

    r = await assession.get('https://httpbin.org/delay/2')
    return r

async def get_delay3():

    r = await assession.get('https://httpbin.org/delay/3')
    return r

t1 = time.perf_counter()
results = assession.run(get_delay1, get_delay2, get_delay3)

for result in results:
    response = result.html.url
    print(response)

t2 = time.perf_counter()
print(f'{t2 - t1} seconds')
