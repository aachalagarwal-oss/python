import asyncio
import time

async def task(name,delay):
    print(f"{name}:started")


    await asyncio.sleep(delay)
    print(f"{name}Resumed after {delay}s")

    await asyncio.sleep(1)
    print(f"{name}:finished")

async def main():
    start=time.time()

    await asyncio.gather(
        task("Task-A",2),
        task("Task-B",1),
        task("Task-C",3),
    )

    end=time.time()

    print(f"Total time :{end-start} seconds")


asyncio.run(main())