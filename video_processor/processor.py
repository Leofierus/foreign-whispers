import whisper
import inflect
import os
import re
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

    data = ''
    for line in lines:
        if '##' in line or line == '\n':
            continue
        else:
            data += line[:-1] + ' '

    if target_language == 'French':
        tts = TTS(model_name='tts_models/fr/css10/vits', progress_bar=True)
        data = convert_data_french(data)
    elif target_language == 'German':
        tts = TTS(model_name='tts_models/de/css10/vits-neon', progress_bar=True)
        data = convert_data_german(data)
    else:
        # More languages not supported yet
        return

    tts.tts_to_file(text=data, file_path=output_path)
    return output_path


def textify(result):
    result = result.replace('@', 'at')
    # Currency symbols
    result = result.replace('€', 'Euro')
    result = result.replace('$', 'Dollar')
    result = result.replace('£', 'Pfund')
    result = result.replace('¥', 'Yen')
    result = result.replace('₹', 'Rupie')
    return result


def convert_data_french(text):
    p = inflect.engine()
    pattern = re.compile(r'(\d+)([.,!?])?')

    def replace(match):
        num = int(match.group(1))
        french_num = p.number_to_words(num, andword="et", zero="zéro")
        return french_num + (match.group(2) if match.group(2) else '')

    result = pattern.sub(replace, text)
    result = result.replace('&', 'et')
    result = result.replace('%', 'pour cent')
    result = result.replace('°', 'degrés')
    return textify(result)


def convert_data_german(text):
    p = inflect.engine()
    pattern = re.compile(r'(\d+)([.,!?])?')

    def replace(match):
        num = int(match.group(1))
        german_num = p.number_to_words(num, andword="und", zero="null")
        return german_num + (match.group(2) if match.group(2) else '')

    result = pattern.sub(replace, text)
    result = result.replace('&', 'und')
    result = result.replace('%', 'Prozent')
    result = result.replace('°', 'Grad')
    return textify(result)
