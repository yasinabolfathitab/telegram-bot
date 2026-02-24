import asyncio
import os
from telethon import TelegramClient, events
from openai import OpenAI

api_id = 31000802
api_hash = "688b80a8860bca0d154d1cb4cceb721f"

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

source_channel = "https://t.me/mad_apes_gambles"
target_channel = "https://t.me/MilyarderZZ"

footer = "\n\n👉 @MilyarderZZ"

client_ai = OpenAI(api_key=OPENAI_KEY)


def clean_text(text):
    if not text:
        return ""

    text = text.replace("Disclaimer", "")
    text = text.replace("Gamble Channel", "")

    return text.strip()


def translate_ai(text):

    try:

        response = client_ai.responses.create(
            model="gpt-4.1-mini",
            input=f"""
متن زیر را به فارسی روان ترجمه کن.
هیچ توضیح اضافه نده.

{text}
"""
        )

        return response.output_text

    except:
        return text


async def main():

    client = TelegramClient("session", api_id, api_hash, connection_retries=None)

    await client.start()

    print("Bot is running...")

    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):

        message = event.message

        text = clean_text(message.text)

        persian_text = translate_ai(text)

        final_text = persian_text + footer

        if message.media:

            await client.send_file(
                target_channel,
                message.media,
                caption=final_text
            )

        else:

            await client.send_message(
                target_channel,
                final_text
            )

    await client.run_until_disconnected()


asyncio.run(main())