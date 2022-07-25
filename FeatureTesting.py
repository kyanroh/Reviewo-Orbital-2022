from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio
import time
from Credentials import API_ID, API_HASH


async def test_signup():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        await client.send_message('ReviewOBot', "/start")
        time.sleep(2)
        await client.send_message('ReviewOBot', '/signup') # Sends signup command
        time.sleep(2)

        # Test for invalid email
        await client.send_message('ReviewOBot', 'hello@g') # Sends an invalid email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends a valid password
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends password confirmation
        time.sleep(2)

        # Test for unmatched password
        await client.send_message('ReviewOBot', 'billy@gmail.com') # Sends an valid email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends a valid password
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends a different password confirmation
        time.sleep(2)

        # Test for pre-existing email in databse already
        await client.send_message('ReviewOBot', 'zychin000@gmail.com') # Sends another pre-existing email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends a valid password
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends the same password confirmation
        time.sleep(2)

        # Test for password shorter than 6 characters
        await client.send_message('ReviewOBot', 'billy@gmail.com') # Sends a valid email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '12356') # Sends a password shorter than 6 characters
        time.sleep(2)
        await client.send_message('ReviewOBot', '12356') # Sends the same password confirmation
        time.sleep(2)

        # Test for success of valid inputs
        await client.send_message('ReviewOBot', 'billy@gmail.com') # Sends another pre-existing email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends a valid password
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends the same password confirmation


async def test_login():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        await client.send_message('ReviewOBot', "/start")
        time.sleep(2)
        await client.send_message('ReviewOBot', '/login') # Sends login command
        time.sleep(2)

        # Test for invalid email
        await client.send_message('ReviewOBot', 'hello@g') # Sends an invalid email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends a valid password
        time.sleep(2)

        # Test for invalid password
        await client.send_message('ReviewOBot', '/login') # Sends login command
        time.sleep(2)
        await client.send_message('ReviewOBot', 'zy@gmail.com') # Sends an valid email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '123@#$') # Sends an invalid password
        time.sleep(2)

        # Test for successful login
        await client.send_message('ReviewOBot', '/login') # Sends login command
        time.sleep(2)
        await client.send_message('ReviewOBot', 'zy@gmail.com') # Sends an valid email 
        time.sleep(2)
        await client.send_message('ReviewOBot', '123456') # Sends an invalid password


async def test_logout():
    async with TelegramClient(StringSession(), API_ID, API_HASH) as client:
        await client.send_message('ReviewOBot', '/logout') # Sends logout command
        time.sleep(2)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_logout())