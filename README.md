
# Song Mashup Downloader

This project allows users to create a custom audio mashup by selecting songs based on a search term. The app downloads the selected songs, extracts parts of them, and creates a mashup. The generated mashup is then sent via email to the user.

## Features

- **Song Search**: Search for songs by a singer’s name.
- **Audio Mashup Creation**: Select the number of songs and the duration of each song segment to be used in the mashup.
- **Email Delivery**: The final mashup is emailed to the user.
- **Responsive Web Interface**: The app provides a user-friendly form to input song search details.

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.6+
- `ffmpeg` installed and configured (for audio processing)
- Flask
- yt-dlp (for downloading audio from YouTube)
- pydub (for audio manipulation)
- smtplib (for sending email)

## Installation

### 1. Clone the repository

Clone this repository to your local machine:

```bash
git clone https://github.com/shaurya-bhatia-sb/Song-Mashup-Downloader.git
cd Song-Mashup-Downloader
```

### 2. Install dependencies

You can install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Configure Email

To send the mashup to an email, you need to configure an email account with app-specific passwords (if using Gmail). 

- **For Gmail**:
  1. Enable [2-Step Verification](https://myaccount.google.com/security) for your Google account.
  2. Generate an **App Password** for your application [here](https://myaccount.google.com/security).
  3. Replace the `EMAIL_ADDRESS` and `EMAIL_PASSWORD` values in `app.py` with your email address and generated app password.

### 4. Configure `ffmpeg`

Make sure you have `ffmpeg` installed and accessible via your system's PATH. If it’s not installed, follow the instructions [here](https://ffmpeg.org/download.html).

Alternatively, you can specify the full path to `ffmpeg` in your script if it’s not added to the PATH.

```python
AudioSegment.ffmpeg = r"path of ffmpeg.exe"  # Modify this line in app.py
```


## Web Preview

### Homepage
![Homepage](Mashup%20songs/screenshots/Homepage.png)

### Success
![Success](Mashup%20songs/screenshots/Success.png)

### Received Mail
![Success](Mashup%20songs/screenshots/Mail.png)



## Usage

1. **Start the Flask Application**

   Run the Flask app:

   ```bash
   python app.py
   ```

2. **Navigate to the web interface**

   Open a web browser and go to:

   ```
   http://127.0.0.1:5000/
   ```

3. **Fill out the form**

   Enter the singer's name, number of songs to download, song segment duration, and your email. 

4. **Download and Receive Mashup**

   After submitting the form, the app will download the selected songs, create the mashup, and email it to you.

## File Structure

```plaintext
/Song-Mashup-Downloader
├── app.py                  # Main Flask application
├── mashup.py                 # Python code
├── requirements.txt        # List of dependencies
├── templates/
│   └── index.html          # HTML form for user interaction
├── static/
│   └── style.css           # Custom CSS for styling the web interface
├── mashups/                # Directory where mashups are stored
└── README.md               # This file
```

## Contributing

If you’d like to contribute to this project, feel free to:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is open-source and available under the MIT License. 

---

Made with ❤️ by Shaurya Bhatia
