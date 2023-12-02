import shutil

import whisper
import inflect
import os
import re
from TTS.api import TTS
from moviepy.editor import VideoFileClip
from pydub import AudioSegment


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


def beautify_entries(subtitle_entries, total_dur):
    final_entries = []
    if subtitle_entries[0]['start'] != 0:
        final_entries.append({"start": 0, "end": subtitle_entries[0]['start'], "text": "<empty>"})

    for i in range(len(subtitle_entries)):
        if i != 0 and subtitle_entries[i - 1]['end'] != subtitle_entries[i]['start']:
            final_entries.append({"start": subtitle_entries[i - 1]['end'], "end": subtitle_entries[i]['start'],
                                  "text": "<empty>"})
        final_entries.append(subtitle_entries[i])

    if subtitle_entries[-1]['end'] != total_dur:
        final_entries.append({"start": subtitle_entries[-1]['end'], "end": total_dur, "text": "<empty>"})

    return final_entries


def beautify_audios(audio_files, original_dur, expected_dur, adjusted_dur):
    has_started = False
    final_files = []
    duration_buffer = 0

    for i in range(len(audio_files)):
        if adjusted_dur[i] == 99999:
            if not has_started:
                final_files.append(AudioSegment.silent(expected_dur[i] * 1000))
                has_started = True
            else:
                if expected_dur[i] * 1000 < duration_buffer:
                    final_files.append(AudioSegment.silent(duration_buffer - (expected_dur[i] * 1000)))
                    duration_buffer -= expected_dur[i] * 1000
                else:
                    final_files.append(AudioSegment.silent((expected_dur[i] * 1000) - duration_buffer))
                    duration_buffer = 0
        elif original_dur[i] > expected_dur[i] * 1000:
            final_files.append(audio_files[i])
            duration_buffer += original_dur[i] - expected_dur[i] * 1000
        else:
            if original_dur[i] + duration_buffer < expected_dur[i] * 1000:
                final_files.append(audio_files[i] + AudioSegment
                                   .silent((expected_dur[i] * 1000) - (original_dur[i] + duration_buffer)))
                duration_buffer = 0
            else:
                final_files.append(audio_files[i] + AudioSegment.silent((expected_dur[i] * 1000) - (original_dur[i])))
                duration_buffer -= (expected_dur[i] * 1000) - (original_dur[i])

    return final_files


def tts_convertor(translated_file, target_language, name):
    output_path = os.path.join("media", f"{name}_{target_language}.wav")
    with open(translated_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    subtitle_entries = []
    original_dur = []
    expected_dur = []
    adjusted_dur = []
    data = ''
    timestamp, start_time, end_time = None, None, None
    duration = VideoFileClip(f"media/{name}.mp4").duration

    for i in range(len(lines)):
        if '##' in lines[i]:
            timestamp = lines[i].replace('## ', '').replace(' :', '').replace(' :\n', '')
            start_time, end_time = map(float, timestamp.split(" - "))
            if lines[i + 1] == '\n':
                subtitle_entries.append({"start": start_time, "end": end_time,
                                         "text": "<empty>"})
        elif lines[i] == '\n':
            continue
        else:
            subtitle_entries.append({"start": start_time, "end": end_time,
                                     "text": lines[i].lstrip() if lines[i].lstrip() != '' else "<empty>"})
            data += lines[i][:-1] + ' '

    final_entries = beautify_entries(subtitle_entries, duration)

    if target_language == 'French':
        tts = TTS(model_name='tts_models/fr/css10/vits', progress_bar=True)
        # data = convert_data_french(data)
        for entry in final_entries:
            entry['text'] = convert_data_french(entry['text'])
    elif target_language == 'German':
        tts = TTS(model_name='tts_models/de/css10/vits-neon', progress_bar=True)
        # data = convert_data_german(data)
        for entry in final_entries:
            entry['text'] = convert_data_german(entry['text'])
    else:
        # More languages not supported yet
        return None

    audio_files = []
    if not os.path.exists(f"media/{name}"):
        os.mkdir(f"media/{name}")

    for entry in final_entries:
        if entry['text'] == "<empty>":
            audio_files.append(AudioSegment.silent(duration=(entry['end'] - entry['start']) * 1000))
            original_dur.append(0)
            expected_dur.append(entry['end'] - entry['start'])
            adjusted_dur.append(99999)
        else:
            tts.tts_to_file(text=entry['text'], file_path=f"media/{name}/{entry['end']}.wav")

            audio_file = AudioSegment.from_wav(f"media/{name}/{entry['end']}.wav")

            original_dur.append(len(audio_file))
            expected_dur.append(entry['end'] - entry['start'])
            adjusted_dur.append(0)

            audio_files.append(audio_file)

    final_files = beautify_audios(audio_files, original_dur, expected_dur, adjusted_dur)

    final_audio = AudioSegment.empty()
    for audio_file in final_files:
        final_audio += audio_file

    final_audio.export(output_path, format="wav")
    shutil.rmtree(f"media/{name}")

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
