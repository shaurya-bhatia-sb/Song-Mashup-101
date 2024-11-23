import os
from yt_dlp import YoutubeDL
from pydub import AudioSegment

# Set up directories
BASE_DIR = os.path.abspath("mashups")
os.makedirs(BASE_DIR, exist_ok=True)

# Path to the mashup file
MASHUP_FILE = os.path.join(BASE_DIR, "mashup.mp3")

# Configure ffmpeg path for pydub
AudioSegment.ffmpeg = r"Path to ffmpeg.exe file"

# Ensure the mashup.mp3 is initialized as a valid file
if not os.path.exists(MASHUP_FILE):
    silent_audio = AudioSegment.silent(duration=1000)  # 1 second of silence
    silent_audio.export(MASHUP_FILE, format="mp3")


# Function to search for songs using youtubesearchpython
def search_songs(singer_name, num_songs=4):
    from youtubesearchpython import VideosSearch
    search_query = f"{singer_name} official music video"
    videos_search = VideosSearch(search_query, limit=num_songs)
    search_results = videos_search.result()
    video_urls = [result['link'] for result in search_results['result']]
    return video_urls


# Function to download and append a segment to the mashup
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
                segment = song[:segment_duration * 1000]  # Extract first `segment_duration` seconds
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


# Main script logic
def main():
    # Get user input
    singer_name = input("Enter the singer's name: ")
    num_songs = int(input("Enter the number of songs for the mashup: "))
    segment_duration = int(input("Enter the duration for each song segment (in seconds): "))

    # Reset the mashup file
    silent_audio = AudioSegment.silent(duration=1000)  # 1 second of silence
    silent_audio.export(MASHUP_FILE, format="mp3")
    print("Initialized mashup.mp3 file.")

    # Search and download songs
    video_urls = search_songs(singer_name, num_songs)
    print(f"Found {len(video_urls)} songs. Starting download...")

    for idx, video_url in enumerate(video_urls):
        temp_file = os.path.join(BASE_DIR, f"temp_song_{idx}.mp3")
        download_and_append(video_url, temp_file, segment_duration)

    print(f"Mashup created successfully! Saved at: {MASHUP_FILE}")


if __name__ == "__main__":
    main()
