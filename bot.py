import asyncio
import os
import re
from telethon import TelegramClient, events
from openai import OpenAI

# ENV VARIABLES
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# کانال ها (فقط یوزرنیم)
source_channel = "mad_apes_gambles"
target_channel = "MilyarderZZ"

footer = "\n\n👉 @MilyarderZZ"

client_ai = OpenAI(api_key=OPENAI_KEY)


def remove_x_links(text):

    pattern = r'https?:\/\/(x\.com|twitter\.com)\/\S+'
    return re.sub(pattern, '', text)


def clean_text(text):

    if not text:
        return ""

    text = remove_x_links(text)

    remove_words = [
        "Disclaimer",
        "Gambles Channel",
        "Dip",
        "Chat",
        "____"
    ]

    for w in remove_words:
        text = text.replace(w, "")

    return text.strip()


def translate_ai(text):

    if not text:
        return ""

    try:

        response = client_ai.responses.create(
            model="gpt-4o-mini",
            input=f"""
Translate the following text to fluent Persian.
Only output the translated Persian text.

{text}
"""
        )

        return response.output_text

    except Exception as e:

        print("Translation error:", e)

        return text


async def main():

    client = TelegramClient("session", api_id, api_hash)

    await client.start()

    print("BOT RUNNING...")

    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):

        try:

            message = event.message

            print("NEW MESSAGE DETECTED")

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
