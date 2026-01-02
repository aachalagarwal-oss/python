import asyncio
import time

async def all_external_api(service_name):
    await asyncio.sleep(2)
    print(f"{service_name} called")
async def main():
    start_time = time.perf_counter()
    await asyncio.gather(
        all_external_api("first api call"),
        all_external_api("second api call"),
        all_external_api("third api call")
    )

    end_time = time.perf_counter()
    print(f"total time taken:{end_time-start_time}seconds")
if __name__ == "__main__":
    asyncio.run(main())