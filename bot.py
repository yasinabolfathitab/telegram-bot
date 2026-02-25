import asyncio
import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from openai import OpenAI

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
openai_key = os.getenv("OPENAI_KEY")

source_channels = [
    "Bitfa_io",
    "Cointelegraph",
    "NeoVestNews"
]
target_channel = "MilyarderZZ"

footer = "\n\n👉 @MilyarderZZ"

ai = OpenAI(api_key=openai_key)


def remove_x_links(text):

    pattern = r'https?:\/\/(x\.com|twitter\.com)\/\S+'
    return re.sub(pattern, '', text)


def clean_text(text):

    if not text:
        return ""

    text = remove_x_links(text)

    remove_words = [
        "LBANK",
        "ثبت نام و لینک ورود",
        "لینک ورود و ثبت نام",
        "Bitfa Futures",
        "@Bitfa_io",
        "YouTube",
        "@NeoVestNews"
    ]

    for w in remove_words:
        text = text.replace(w, "")

    return text.strip()


def translate_ai(text):

    if not text:
        return ""

    try:

        response = ai.responses.create(
            model="gpt-4o-mini",
            input=f"""
Translate the following text to fluent Persian.
Return only the Persian translation.

{text}
"""
        )

        return response.output_text

    except Exception as e:

        print("Translation error:", e)

        return text


async def main():

    client = TelegramClient(
        StringSession(string_session),
        api_id,
        api_hash
    )

    await client.start()

    print("BOT RUNNING")

    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):

        try:

            message = event.message

            print("NEW POST")

            text = clean_text(message.text)

            translated = translate_ai(text)

            final_text = translated + footer

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

            print("POST SENT")

        except Exception as e:

            print("POST ERROR:", e)


    await client.run_until_disconnected()


asyncio.run(main())



