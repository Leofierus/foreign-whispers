import whisper
import os
from TTS.api import TTS
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
            start = f"{segment['start']:.2f}"
            end = f"{segment['end']:.2f}"
            transcript_file.write(f"## {start} - {end} :\n{text}\n\n")
    return transcript_path


def tts_convertor(translated_file, target_language, name):
    output_path = os.path.join("media", f"{name}_{target_language}.wav")
    with open(translated_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text = ''
    for line in lines:
        if '##' in line or line == '\n':
            continue
        else:
            text += line[:-1] + ' '

    if target_language == 'French':
        tts = TTS(model_name='tts_models/fr/mai/tacotron2-DDC', progress_bar=True)

    elif target_language == 'German':
        tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=True)
    else:
        return

    tts.tts_to_file(text=text, path="output.wav")
    source_file = "output.wav"
    if os.path.exists(source_file):
        directory = "media"
        new_filename = f"{name}_{target_language}.wav"
        destination = os.path.join(directory, new_filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.rename(source_file, destination)
    return output_path
