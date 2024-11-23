import os
from flask import Flask, request, render_template
from youtubesearchpython import VideosSearch
from yt_dlp import YoutubeDL
from pydub import AudioSegment
from email.message import EmailMessage
import smtplib

app = Flask(__name__)

# Define directories
BASE_DIR = os.path.abspath("mashups")
os.makedirs(BASE_DIR, exist_ok=True)

# Path to the preloaded mashup file
MASHUP_FILE = os.path.join(BASE_DIR, "mashup.mp3")

# Email sender configuration
EMAIL_ADDRESS = "your email" # Replace with your email
EMAIL_PASSWORD = "your app password"      # Replace with the generated app password

# Set ffmpeg path for pydub
AudioSegment.ffmpeg = r"path to ffmpeg.exe"
# Confirm FFmpeg path
print("FFmpeg Path:", AudioSegment.ffmpeg)

# Create an empty mashup file before processing begins
if not os.path.exists(MASHUP_FILE):
    silent_audio = AudioSegment.silent(duration=1000)  # 1 second of silence to create a valid mp3
    silent_audio.export(MASHUP_FILE, format="mp3")


# Search for songs using youtubesearchpython
def search_songs(singer_name, num_songs=4):
    search_query = f"{singer_name} official music video"
    videos_search = VideosSearch(search_query, limit=num_songs)
    search_results = videos_search.result()
    video_urls = [result['link'] for result in search_results['result']]
    return video_urls


# Download audio and append a segment to the mashup
def download_and_append(video_url, temp_filename, segment_duration=15):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': temp_filename,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
            print(f"Downloaded: {temp_filename}")

        # Check if the file is valid
        if os.path.getsize(temp_filename) > 0:
            try:
                song = AudioSegment.from_file(temp_filename)
                segment = song[:segment_duration * 1000]  # Extract the first `segment_duration` seconds
                mashup = AudioSegment.from_file(MASHUP_FILE)
                updated_mashup = mashup + segment
                updated_mashup.export(MASHUP_FILE, format="mp3")
                print(f"Appended {segment_duration} seconds to mashup.mp3")
            except Exception as audio_error:
                print(f"Error processing audio file {temp_filename}: {audio_error}")
        else:
            print(f"Downloaded file {temp_filename} is empty or invalid.")

        # Clean up temp file
        os.remove(temp_filename)

    except Exception as e:
        print(f"Error downloading or processing {video_url}: {e}")


# Send the mashup via email
def send_email(receiver_email, mashup_file):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Your Mashup File"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = receiver_email
        msg.set_content("Please find your mashup file attached.")

        # Attach the mashup file
        with open(mashup_file, "rb") as file:
            msg.add_attachment(file.read(), maintype="audio", subtype="mp3", filename=os.path.basename(mashup_file))

        # Send the email using SMTP with the app password
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Use app password
            server.send_message(msg)

        print("Email sent successfully.")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer_name = request.form.get("singer")
        num_songs = int(request.form.get("num_songs", 4))
        segment_duration = int(request.form.get("segment_duration", 15))
        receiver_email = request.form.get("email")

        try:
            # Reset the mashup file to empty at the start
            silent_audio = AudioSegment.silent(duration=1000)  # 1 second of silence
            silent_audio.export(MASHUP_FILE, format="mp3")

            # Search for songs
            video_urls = search_songs(singer_name, num_songs)

            # Download and process each song incrementally
            for idx, video_url in enumerate(video_urls):
                temp_file = os.path.join(BASE_DIR, f"temp_song_{idx}.mp3")
                download_and_append(video_url, temp_file, segment_duration)

            # Send the mashup file via email
            if send_email(receiver_email, MASHUP_FILE):
                return "Mashup created and emailed successfully!"
            else:
                return "Mashup created, but there was an error sending the email."

        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred. Please try again."

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
