# Foreign Whispers - YouTube Video Downloader

Foreign Whispers is a Django web application that allows users to download YouTube videos and their associated captions and transcripts.

## Installation

1. Clone the repository to your local machine.
2. Create a Python virtual environment and activate it.
3. Install project dependencies using `pip install -r requirements.txt`.
4. Run Django migrations: `python manage.py migrate`.
5. Start the development server: `python manage.py runserver`.
6. Access the application in your web browser at [http://localhost:8000/video_downloader/download](http://localhost:8000/video_downloader/download/).

## Usage

1. Visit the homepage and provide a YouTube video URL.
2. Click the "Download" button to initiate the download process.
3. The video, captions (if available), and transcript (if necessary) will be saved in the 'media/' directory.

## Project Structure

- `video_downloader/`: Django app containing views, models, and templates.
- `media/`: Directory for storing downloaded videos, captions, and transcripts.
- `templates/`: HTML templates used in the project.

## Project Screenshots

### Milestone 1
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/d0e3fcac-bd56-4aa2-846f-4bbd6e03b50d)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/c5b10734-8e21-4a69-9e43-38b7dafae349)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/1fc2c275-4161-499f-bb95-e8dd96e912c8)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/704e92ed-1146-4af5-ad6f-10089de3afe1)


## Team Members
- Malhar Patel (mkp6112@nyu.edu)
- Ruben Garcia (rg4352@nyu.edu)

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or support, please contact [Malhar Patel](mailto:malhar.p@nyu.com).

