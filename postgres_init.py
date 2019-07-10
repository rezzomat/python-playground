from postgres.listeners import main
import asyncio

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

