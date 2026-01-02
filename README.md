# Pseudo-Youtube

Visual and functional likeness of Youtube built with Django for practice and learning purposes and developed over the course of a month, starting from September 2025. It aims to replicate basic key features of Youtube, such as video uploads and playback,
channel creation and comment system. It also has a built in mock livestream of "lofi hip hop radio beats to relax/study to" by the Youtube channel Lofi Girl.

Disclaimer: For the purpose of replicating Youtube, this project utilizes the logos of Youtube and Google, as well as various channel names and icons. However, it is strictly for educational purposes only
and the creator and the project is not affiliated with or endorsed by any of the parties mentioned.

## Features

- User authentication and account management
- Channel creation and management
- Video upload functionality
- Video playback with basic controls
- Commenting system
- Livestreaming demo

## Screenshots
Home screen
<img width="1902" height="995" alt="Screenshot (1370)" src="https://github.com/user-attachments/assets/84d105c5-d740-4c78-866d-5dc21be0cce4" />

Channel page
<img width="1900" height="995" alt="Screenshot (1375)" src="https://github.com/user-attachments/assets/17551cfc-af6b-4298-8b68-67238f22a122" />

Video playback page
<img width="1903" height="976" alt="Screenshot (1372)" src="https://github.com/user-attachments/assets/938174fc-27c3-4882-90d9-7a17686eb470" />

Creator page
<img width="1903" height="992" alt="Screenshot (1373)" src="https://github.com/user-attachments/assets/15eb7829-fee4-453f-9d43-b02d040d0265" />

New channel form
<img width="1900" height="991" alt="Screenshot (1374)" src="https://github.com/user-attachments/assets/5fde4838-629b-4e9e-9be7-7019e54b0604" />

## Installation

1. Clone the repo and navigate to the project folder:
```
git clone https://github.com/NevVaek/Pseudo-Youtube.git
cd mock-youtube
```
   
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up the database:
```
python manage.py migrate
```

4. Run the server:
```
.venv/Scripts/Activate.ps1
python manage.py runserver
```
## Running the livestream:
The mock Lofi Girl Radio utilizes the free and open-source software FFmpeg for video processing and encoding. It requires the ffmpeg on your computer.
Download it here: https://ffmpeg.org/download.html

Note: This repository does not contain the video or the audio files for the livestream.  

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
