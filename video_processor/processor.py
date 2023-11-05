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
    segments = transcript.get('segments') if 'segments' in transcript else []

    transcript_path = audio_path.replace(".mp3", "_whisper.txt")

    with open(transcript_path, 'w', encoding='utf-8') as transcript_file:    
        for segment in segments:
            text = segment['text'].lstrip()
            # Use a precision of 2 decimal places
            start = f"{segment['start']:.2f}"
            end = f"{segment['end']:.2f}"
            transcript_file.write(f"{start} - {end} :\n{text}\n\n")
    return transcript_path
