from rabbit import sender
import asyncio

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sender.async_msg_local(loop))
    # sender.sync_msg_remote()

