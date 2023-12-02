import ffmpeg
import os

from datetime import timedelta
from django.shortcuts import render
from requests import RequestException

from video_processor.processor import extract_audio, transcribe_audio, tts_convertor
from .forms import VideoDownloadForm
from .models import Video
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable, PytubeError
from youtube_transcript_api import YouTubeTranscriptApi
from translator.utils import translate_file


def convert_to_srt(extracted_transcript, language):
    with open(extracted_transcript, 'r') as file:
        lines = file.readlines()

    subtitles = []
    index = 1
    for i in range(0, len(lines)):
        if '##' in lines[i]:
            time_interval = (lines[i].strip().replace(" - ", " --> ")
                             .replace("## ", "").replace(" :", ""))
            time_intervall = time_interval.split(" --> ")
            start_delta = timedelta(seconds=float(time_intervall[0]))
            formatted_time = str(start_delta).split(".")[0]
            milliseconds = str(int(start_delta.microseconds / 1000)).zfill(3)
            time_intervall[0] = f"{formatted_time},{milliseconds}"

            end_delta = timedelta(seconds=float(time_intervall[1]))
            formatted_time = str(end_delta).split(".")[0]
            milliseconds = str(int(end_delta.microseconds / 1000)).zfill(3)
            time_intervall[1] = f"{formatted_time},{milliseconds}"

            time_interval = " --> ".join(time_intervall)

            text = lines[i + 1].strip()
            subtitle = f"{index}\n{time_interval}\n{text}\n\n"
            index += 1
            subtitles.append(subtitle)

    output_file = extracted_transcript.replace(".txt", ".srt").replace(f"_whisper_{language}", "")
    with open(output_file, 'w') as file:
        file.writelines(subtitles)

    return output_file


def embed_subs(video_path, extracted_transcript, language):
    srt_path = convert_to_srt(extracted_transcript, language)
    new_path = video_path.replace(".mp4", "_subbed.mp4")
    try:
        os.remove(new_path)
    except OSError:
        pass
    ffmpeg.input(video_path).filter('subtitles', srt_path).output(new_path).run()
    return new_path


def download_video(request):
    if request.method == 'POST':
        form = VideoDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            target_language = form.cleaned_data['target_language']

            try:
                yt = YouTube(video_url)
                video = yt.streams.get_highest_resolution()
                name = yt.video_id
                video.download(filename='media/' + name + '.mp4')

                transcript_filename = f"{name}_transcript.txt"
                transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)
                transcript_file_path = "media/" + transcript_filename

                with open(transcript_file_path, 'w', encoding='utf-8') as transcript_file:
                    for entry in transcript:
                        transcript_file.write(f"## {entry['start']:.2f} - {(entry['start']+entry['duration']):.2f}")
                        transcript_file.write(f":\n{entry['text']}\n\n")

                # Create a new Video object in the database if same video is not already downloaded
                Video.objects.filter(title=yt.title).delete()
                Video.objects.create(
                    title=yt.title,
                    video_url=video_url,
                    downloaded_video_path=f"media/{name}.mp4",
                    downloaded_transcript_path=f"media/{transcript_filename}"
                )

                # Extract audio from the downloaded video
                extracted_audio = extract_audio(f"media/{name}.mp4")
                Video.objects.filter(title=yt.title).update(extracted_audio_path=extracted_audio)

                # Use whisper to transcribe the audio
                extracted_transcript = transcribe_audio(extracted_audio)
                Video.objects.filter(title=yt.title).update(extracted_transcript_path=extracted_transcript)

                # Use t5-model to translate the transcript
                translated_file = translate_file(extracted_transcript, target_language)
                Video.objects.filter(title=yt.title).update(translated_transcript_path=translated_file)
                embedded_video = embed_subs(f"media/{name}.mp4", extracted_transcript, target_language)
                Video.objects.filter(title=yt.title).update(embedded_video_path=embedded_video)

                # Use TTS API to generate the audio files
                audio_file = tts_convertor(translated_file, target_language, name)
                if target_language == 'French':
                    Video.objects.filter(title=yt.title).update(french_tts_audio_path=audio_file)
                elif target_language == 'German':
                    Video.objects.filter(title=yt.title).update(german_tts_audio_path=audio_file)

                return download_status(request, True, None, name)

            except (RegexMatchError, VideoUnavailable, PytubeError, RequestException) as e:
                error_message = str(e)
                return download_status(request, False, download_error=error_message)
    else:
        form = VideoDownloadForm()

    return render(request, 'downloader.html', {'form': form})


def download_status(request, download_success, download_error=None, new_filename=None):
    context = {
        'download_success': download_success,
        'download_error': download_error,
        'new_filename': new_filename,
    }
    return render(request, 'downloader.html', context)
