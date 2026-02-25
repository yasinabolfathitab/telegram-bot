import asyncio
import os
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from openai import OpenAI

# =========================
# ENV VARIABLES
# =========================

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# =========================
# OPENAI
# =========================

client_ai = OpenAI(api_key=OPENAI_KEY)

# =========================
# CHANNELS
# =========================

source_channels = [
    "Bitfa_io",
    "Cointelegraph",
    "NeoVestNews"
]

target_channel = "MilyarderZZ"

footer = "\n\n👉 @MilyarderZZ"

# =========================
# REMOVE X LINKS
# =========================

def remove_x_links(text):

    pattern = r'https?:\/\/(x\.com|twitter\.com)\/\S+'
    return re.sub(pattern, '', text)

# =========================
# CLEAN TEXT
# =========================

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

# =========================
# AI TRANSLATION
# =========================

def translate_ai(text):

    if not text:
        return ""

    try:

        response = client_ai.responses.create(
            model="gpt-4o-mini",
            input=f"""
Translate the following text to fluent Persian.
Only output Persian translation.

{text}
"""
        )

        return response.output_text

    except Exception as e:

        print("Translation error:", e)
        return text

# =========================
# MAIN
# =========================

async def main():

    client = TelegramClient(
        StringSession(string_session),
        api_id,
        api_hash
    )

    await client.start()

    print("BOT RUNNING...")

    @client.on(events.NewMessage(chats=source_channels))
    async def handler(event):

        try:

            message = event.message

            print("NEW MESSAGE DETECTED")

            text = clean_text(message.text)

            if not text and not message.media:
                return

            translated = translate_ai(text)

            final_text = translated + footer

            await asyncio.sleep(2)

            if message.media:

                await client.send_file(
                    target_channel,
                    message.media,
                    caption=final_text if final_text.strip() else footer
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
