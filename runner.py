import asyncio
from time import sleep
import schedule

from golden_apple import main


def run():
    asyncio.run(main())


schedule.every().day.at('15:02').do(run)
if __name__ == '__main__':
    while True:
        schedule.run_pending()
        sleep(1)
