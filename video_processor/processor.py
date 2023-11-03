import whisper
from moviepy.editor import VideoFileClip


def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio_path = video_path.replace(".mp4", ".mp3")
    audio.write_audiofile(audio_path)
    return audio_path


def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    transcript = whisper.transcribe(model, audio_path)
    transcript_path = audio_path.replace(".mp3", "_whisper.txt")
    transcript_str = str(transcript)
    with open(transcript_path, 'w', encoding='utf-8') as transcript_file:
        transcript_file.write(transcript_str)
    return transcript_path
