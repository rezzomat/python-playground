import asyncpg
import config
import uuid
import asyncio
from asyncpg.exceptions import UniqueViolationError
import pika


def generate_uuid():
    return str(uuid.uuid4())


class TestTable:

    def __init__(self, pg):
        self.pg = pg

    async def insert(self, key, value):
        await self.pg.execute("INSERT INTO test_table (id, key, value) VALUES ($1, $2, $3)", generate_uuid(), key, value)

    async def update(self, id, key, value):
        await self.pg.execute("UPDATE test_table SET key = $2, value = $3 WHERE id = $1", id, key, value)

    async def get_by_id(self, id):
        return await self.pg.fetchrow("SELECT * FROM test_table WHERE id = $1", id)

    async def get_by_key(self, key):
        return await self.pg.fetchrow("SELECT * FROM test_table WHERE key = $1", key)


async def main():
    pg = await asyncpg.connect(host=config.pg_host, user=config.pg_user, password=config.pg_password,
                               database=config.pg_database)

    test_table = TestTable(pg)
    try:
        await test_table.insert('test', 'hello world')
    except UniqueViolationError as e:
        print(e)

    entry = await test_table.get_by_key('test')
    print(entry)

    q1 = asyncio.Queue()

    def listener(*args):
        credentials = pika.PlainCredentials(config.mq_user, config.mq_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(config.mq_host, config.mq_port, '/', credentials))
        channel = connection.channel()

        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body='sync Hello World!')
        print(" [x] Sent 'Hello World!'")

    await pg.add_listener('test', listener)
    await pg.execute("NOTIFY test, 'aaaa'")

    await q1.get()

