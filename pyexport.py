from pyrogram import Client
from pyrogram.types import Message
from datetime import datetime

app = Client(
    "my_bot_session",  # Replace with your session name
    api_hash="your_api_hash",
    api_id=12345,       # Replace with your API ID
    phone_number="your_phone_number",
    password="your_password"  # Leave empty if you don't have two-step verification
)

@app.on_message()
async def on_message(app: Client, message: Message):
    if message.text == "export":
        me = await app.get_me()
        chat_id = message.chat.id
        user = await app.get_chat(chat_id=chat_id)
        await app.send_message(chat_id, "Exporting chat data...")

        messages = []

        async for msg in app.get_chat_history(chat_id):
            messages.append(msg)

        messages.reverse()

        with open(f"Export - {chat_id}.html", "w", encoding="utf-8") as html_file:
            html_file.write('<html><head><title>Chat Export | Sepehr0Day</title>')
            html_file.write('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/5.3.1/css/bootstrap.min.css">')

            html_file.write('<style>')
            html_file.write('body { background-color: #f0f0f0; }')
            html_file.write('.container { max-width: 800px; margin: 0 auto; background-color: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.2); }')
            html_file.write('.message-box { padding: 10px; margin: 10px; border-radius: 5px; }')
            html_file.write('.sender-box { background-color: #5bc0de; color: #fff; text-align: left; }')
            html_file.write('.receiver-box { background-color: #337ab7; color: #fff; text-align: right; }')
            html_file.write('.message-time { font-size: 10px; color: #777; text-align: right; }')
            html_file.write('</style></head><body class="bg-primary">')
            html_file.write('<div class="container">')
            html_file.write(f'<div class="alert alert-info" style="text-align: center;"><strong>Person Info:</strong><br> Name: {user.first_name}<br> Username: {user.username}<br> User ID: {user.id}<br> Bio: {user.bio}<br></div>')

            for msg in messages:
                box_class = ""
                if msg.from_user and msg.from_user.id == me.id:
                    box_class = 'sender-box'
                else:
                    box_class = 'receiver-box'

                html_file.write(f'<div class="message-box {box_class}">')

                sender_name = msg.from_user.first_name if msg.from_user else "Unknown"
                html_file.write(f'<strong>{sender_name}:</strong><br>')

                timestamp = msg.date.timestamp()
                message_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                html_file.write(f'<span class="message-time">{message_time}</span><br>')


                if msg.text:
                    html_file.write(f'{msg.text}')
                if msg.photo:
                    photo_file = await app.download_media(msg.photo.file_id, file_name=f"{msg.photo.file_id}.jpg")
                    html_file.write(f'<img src="{photo_file}" alt="Photo" class="img-fluid" style="height: auto; max-width: 100%;">')
                if msg.video:
                    video_file = await app.download_media(msg.video.file_id, file_name=f"{msg.video.file_id}.mp4")
                    html_file.write(f'<video controls class="img-fluid"><source src="{video_file}" type="video/mp4" style="height: auto; max-width: 100%;"></video>')
                if msg.voice:
                    voice_file = await app.download_media(msg.voice.file_id, file_name=f"{msg.voice.file_id}.mp3")
                    html_file.write(f'<audio controls ><source src="{voice_file}" type="audio/mpeg"></audio>')
                if msg.audio:
                    audio_file = await app.download_media(msg.audio.file_id, file_name=f"{msg.audio.file_id}.mp3")
                    html_file.write(f'<audio controls ><source src="{audio_file}" type="audio/mpeg"></audio>')
                if msg.animation:
                    animation_file = await app.download_media(msg.animation.file_id, file_name=f"{msg.animation.file_id}.gif")
                    html_file.write(f'<video controls class="img-fluid"><source src="{animation_file}" type="video/mp4" style="height: auto; max-width: 100%;"></video>')
                if msg.document:
                        document_file = await app.download_media(msg.document.file_id, file_name=msg.document.file_name)
                        html_file.write(f'<a href="{document_file}" download="{msg.document.file_name}" class="btn btn-info">{msg.document.file_name}</a>')
                html_file.write('</div>')
            html_file.write('</div>')
            html_file.write("</body></html>")
            html_file.close()
        await app.send_message(chat_id, f"Chat data export complete.\nFile Name : Export - {chat_id}.html")
app.run()