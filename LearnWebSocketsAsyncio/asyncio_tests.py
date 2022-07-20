import asyncio


async def doSomethingAsync():
    await asyncio.sleep(1)
    return 1


async def generateAsync():
    for i in range(5):
        yield i
        await asyncio.sleep(0.5)


async def async_main():
    print('Awaiting async:')
    x = await doSomethingAsync()
    print(f'Done! {{res: {x}}}')


async def async_main_with_generator():
    print('running async generator...')
    async for x in generateAsync():
        print(f'{x} ', end='')
    print('done!')

def main_python_3_7(async_fn):
    asyncio.run(async_fn())


def main_python_3_6(async_fn):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_fn())


if __name__ == '__main__':
    # main_python_3_7(async_main)
    # main_python_3_6(async_main)

    main_python_3_7(async_main_with_generator)