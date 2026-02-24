import asyncio
import os
import re
from telethon import TelegramClient, events
from openai import OpenAI

# ENV
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
OPENAI_KEY = os.getenv("OPENAI_KEY")

source_channel = "https://t.me/mad_apes_gambles"
target_channel = "https://t.me/MilyarderZZ"

footer = "\n\n👉 @MilyarderZZ"

client_ai = OpenAI(api_key=OPENAI_KEY)


# حذف لینک های X
def remove_x_links(text):

    pattern = r'https?:\/\/(x\.com|twitter\.com)\/\S+'
    return re.sub(pattern, '', text)


# پاکسازی متن
def clean_text(text):

    if not text:
        return ""

    text = remove_x_links(text)

    words_to_remove = [
        "Disclaimer",
        "Gambles Channel",
        "Dip",
        "Chat",
        "____"
    ]

    for w in words_to_remove:
        text = text.replace(w, "")

    return text.strip()


# تشخیص انگلیسی بودن متن
def is_english(text):

    english_chars = re.findall(r'[a-zA-Z]', text)

    if len(english_chars) > 10:
        return True

    return False


# ترجمه با AI
def translate_ai(text):

    if not text:
        return ""

    if not is_english(text):
        return text

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

    except Exception as e:

        print("Translation Error:", e)

        return text


async def main():

    client = TelegramClient("newsession", api_id, api_hash)

    await client.start()

    print("Bot is running...")

    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):

        try:

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

        except Exception as e:

            print("Post Error:", e)


    await client.run_until_disconnected()


asyncio.run(main())
