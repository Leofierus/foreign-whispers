# Foreign Whispers - YouTube Video Downloader

Foreign Whispers is a Django web application that allows users to download YouTube videos and their associated captions and transcripts along with extracting the audio from the file and then using [whisper](https://github.com/openai/whisper) library to transcribe the audio file.

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

<details>
<summary>Milestone 1</summary>
  
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/d0e3fcac-bd56-4aa2-846f-4bbd6e03b50d)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/c5b10734-8e21-4a69-9e43-38b7dafae349)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/1fc2c275-4161-499f-bb95-e8dd96e912c8)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/704e92ed-1146-4af5-ad6f-10089de3afe1)
</details>

<details>
<summary>Milestone 2</summary>
  
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/84728d52-3755-4024-8d8a-298f3d56f51a)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/c5b10734-8e21-4a69-9e43-38b7dafae349)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/eaf2baad-9eab-4e5d-9bc4-0c528e12c769)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/8bd6070b-dafd-4be5-adcd-24b85a60e9a2)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/b0c984ff-3d44-4e92-ba20-87c0ab5ce9e7)
</details>

<details>
<summary>Milestone 3</summary>
  
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/ba3b6673-08d0-4eed-bc71-f159d0ae3029)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/89ad2b5a-f262-4ecf-a7b4-1a556b2d2d6e)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/bca1c8d2-b6f9-4c25-912d-ee1d0632f881)
</details>

<details>
<summary>Milestone 4</summary>

</details>

## Team Members
- Malhar Patel (mkp6112@nyu.edu)
- Ruben Garcia (rg4352@nyu.edu)

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or support, please contact [Malhar Patel](mailto:malhar.p@nyu.com).

