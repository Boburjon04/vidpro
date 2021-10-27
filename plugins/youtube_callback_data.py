import asyncio
import os
import time

from pyrogram import (Client,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup,
                      ContinuePropagation,
                      InputMediaDocument,
                      InputMediaVideo,
                      InputMediaAudio)

from helper.ffmfunc import duration
from helper.ytdlfunc import downloadvideocli, downloadaudiocli
from PIL import Image
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from plugins.display_progress import progress_for_pyrogram, humanbytes, TimeFormatter

@Client.on_callback_query()
async def catch_youtube_fmtid(c, m):
    cb_data = m.data
    if cb_data.startswith("ytdata||"):
        yturl = cb_data.split("||")[-1]
        format_id = cb_data.split("||")[-2]
        media_type = cb_data.split("||")[-3].strip()
        print(media_type)
        if media_type == 'audio':
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton(
                "Audio", callback_data=f"{media_type}||{format_id}||{yturl}"), InlineKeyboardButton("Document",
                                                                                                    callback_data=f"docaudio||{format_id}||{yturl}")]])
        else:
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton(
                "Video", callback_data=f"{media_type}||{format_id}||{yturl}"), InlineKeyboardButton("Document",
                                                                                                    callback_data=f"docvideo||{format_id}||{yturl}")]])

        await m.edit_message_reply_markup(buttons)

    else:
        raise ContinuePropagation


@Client.on_callback_query()
async def catch_youtube_dldata(c, q):
    cb_data = q.data.strip()
    #print(q.message.chat.id)
    # Callback Data Check
    yturl = cb_data.split("||")[-1]
    format_id = cb_data.split("||")[-2]
    thumb_image_path = "/app/downloads" + \
        "/" + str(q.message.chat.id) + ".jpg"
    print(thumb_image_path)
    if os.path.exists(thumb_image_path):
        width = 0
        height = 0
        metadata = extractMetadata(createParser(thumb_image_path))
        #print(metadata)
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")
        img = Image.open(thumb_image_path)
        if cb_data.startswith(("audio", "docaudio", "docvideo")):
            img.resize((320, height))
        else:
            img.resize((90, height))
        img.save(thumb_image_path, "JPEG")
     #   print(thumb_image_path)
    if not cb_data.startswith(("video", "audio", "docaudio", "docvideo")):
        print("no data found")
        raise ContinuePropagation

    filext = "%(title)s.%(ext)s"
    userdir = os.path.join(os.getcwd(), "downloads", str(q.message.chat.id))

    if not os.path.isdir(userdir):
        os.makedirs(userdir)
    chunk = await response.content.read(Config.CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += Config.CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**Download Status**
URL: {}
File Size: {}
Downloading: {}
ETA: {}""".format(
    url,
    humanbytes(total_length),
    humanbytes(downloaded),
    TimeFormatter(estimated_total_time)
)
                        if current_message != display_message:
                            await bot.edit_message_text(
                                chat_id,
                                message_id,
                                text=current_message
                            )
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()
    filepath = os.path.join(userdir, filext)
    # await q.edit_message_reply_markup([[InlineKeyboardButton("Tayyorlanmoqda..")]])

    audio_command = [
        "youtube-dl",
        "-c",
        "--prefer-ffmpeg",
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", format_id,
        "-o", filepath,
        yturl,

    ]

    video_command = [
        "youtube-dl",
        "-c",
        "--embed-subs",
        "-f", f"{format_id}+bestaudio",
        "-o", filepath,
        "--hls-prefer-ffmpeg", yturl]

    loop = asyncio.get_event_loop()

    med = None
    if cb_data.startswith("audio"):
        filename = await downloadaudiocli(audio_command)
        med = InputMediaAudio(
            media=filename,
            thumb=thumb_image_path,
            caption=os.path.basename(filename),
            title=os.path.basename(filename)
        )

    if cb_data.startswith("video"):
        filename = await downloadvideocli(video_command)
        dur = round(duration(filename))
        med = InputMediaVideo(
            media=filename,
            duration=dur,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=os.path.basename(filename),
            supports_streaming=True
        )

    if cb_data.startswith("docaudio"):
        filename = await downloadaudiocli(audio_command)
        med = InputMediaDocument(
            media=filename,
            thumb=thumb_image_path,
            caption=os.path.basename(filename),
        )

    if cb_data.startswith("docvideo"):
        filename = await downloadvideocli(video_command)
        dur = round(duration(filename))
        med = InputMediaDocument(
            media=filename,
            thumb=thumb_image_path,
            caption=os.path.basename(filename),
        )
    if med:
        loop.create_task(send_file(c, q, med, filename))
    else:
        print("med not found")


async def send_file(c, q, med, filename):
    print(med)
    try:
        await q.edit_message_reply_markup(
            InlineKeyboardMarkup([[InlineKeyboardButton("Video yuborilmoqda...", callback_data="down")]]))
        await c.send_chat_action(chat_id=q.message.chat.id, action="upload_document")
        # this one is not working
        await q.edit_message_media(media=med)
    except Exception as e:
        print(e)
        await q.edit_message_text(e)
    finally:
        try:
            os.remove(filename)
            os.remove(thumb_image_path)
        except:
            pass