# Foreign Whispers - YouTube Video Downloader

Foreign Whispers is a Django web application that allows users to download YouTube videos with captions and transcripts in multiple languages along with a bunch of AI models to translate the generated text to the user-desired language. The application uses the [pytube](https://pytube.io/) library to download videos and captions, and the [whisper](https://github.com/openai/whisper) library to generate transcripts. The application also uses the [Mozilla TTS](https://tts.readthedocs.io/en/latest/tutorial_for_nervous_beginners.html) library to generate audio files from the transcripts and a mix of [librosa](https://librosa.org/), [soundfile](https://python-soundfile.readthedocs.io/en/0.11.0/) and [moviepy](https://zulko.github.io/moviepy/) to embed the audio file into the video.

## YouTube Demo Link
https://youtu.be/3plIfwKIbFQ

## Example outputs of the application
1. English to French: [Drive Link](https://drive.google.com/file/d/1Bulh9-KI_4KIDMoORQqxYUGn4zX2sFqL/view?usp=sharing)
2. English to German: [Drive Link](https://drive.google.com/file/d/1_aJITS4zPovRrP60tHlpvwf2Z85H3jkE/view?usp=sharing)


## Installation

1. Clone the repository to your local machine.
2. Create a Python virtual environment and activate it.
3. Install project dependencies using `pip install -r requirements.txt`.
4. It also requires [rubberband](https://breakfastquay.com/rubberband/index.html) to be installed on your system.
5. Run Django migrations: `python manage.py migrate`.
6. Start the development server: `python manage.py runserver`.
7. Access the application in your web browser at [http://localhost:8000/video_downloader/download](http://localhost:8000/video_downloader/download/).

## Usage

1. Visit the homepage and provide a YouTube video URL.
2. Click the "Download" button to initiate the download process.
3. The video, captions (if available), and transcript (if necessary) will be saved in the `media/` directory.

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
The application will return an audio file within the media directory of the selected translation in a .wav format.
<img width="1440" alt="Screenshot 2023-11-26 at 3 48 38 PM" src="https://github.com/Leofierus/foreign-whispers/assets/143608003/5d8272a9-3571-4c11-8dad-318b594039e9">
<img width="1440" alt="Screenshot 2023-11-26 at 3 49 11 PM" src="https://github.com/Leofierus/foreign-whispers/assets/143608003/5115426f-53d6-4118-81d5-f237e322c6d9">
</details>

<details>
<summary>Milestone 5</summary>
  
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/655f6dff-34d6-4034-a99e-c64f1c64a158)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/4d28cfbd-e063-403a-b11a-42301c088820)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/10009143-07b7-437c-bfb1-ef7b00e2b3c7)
![image](https://github.com/Leofierus/foreign-whispers/assets/51908556/e0276f15-a970-42e6-a50a-5036a2e7e85a)
![image](https://github.com/Leofierus/foreign-whispers/assets/143608003/15dc22a5-78ad-4ecd-a5a0-cff99bc8b6d2)
![image](https://github.com/Leofierus/foreign-whispers/assets/143608003/fd555029-56bb-4476-8ab5-7e3ef4e47bc2)
![image](https://github.com/Leofierus/foreign-whispers/assets/143608003/1625b385-7cfb-47ac-907a-51d62b8c8f36)

</details>

## Team Members
- Malhar Patel (mkp6112@nyu.edu)
- Ruben Garcia (rg4352@nyu.edu)

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For questions or support, please contact [Malhar Patel](mailto:malhar.p@nyu.com).

