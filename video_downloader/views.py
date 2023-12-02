import ffmpeg
import os

from datetime import timedelta

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
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

    subtitles = srt_convertor(lines)

    output_file = extracted_transcript.replace(".txt", ".srt").replace(f"_whisper_{language}", "")
    with open(output_file, 'w') as file:
        file.writelines(subtitles)

    return output_file


def embed_subs_audio(video_path, extracted_transcript, audio_file, language):
    srt_path = convert_to_srt(extracted_transcript, language)
    new_path = video_path.replace(".mp4", "_subbed.mp4")
    newer_path = video_path.replace(".mp4", "_dubbed.mp4")
    try:
        os.remove(new_path)
    except OSError:
        pass
    ffmpeg.input(video_path).filter('subtitles', srt_path).output(new_path).run()

    video_clip = VideoFileClip(new_path)
    audio_clip = AudioFileClip(audio_file)
    if audio_clip.duration > video_clip.duration:
        print(audio_clip.duration)
        print(video_clip.duration)

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(newer_path)
    return newer_path


def paginate_data(request, extracted_transcript, translated_file, param):
    with open(extracted_transcript, 'r', encoding='utf-8') as file:
        extracted = file.readlines()

    with open(translated_file, 'r', encoding='utf-8') as file:
        translated = file.readlines()

    data = []
    for i in range(0, len(extracted)):
        if '##' in extracted[i]:
            timestamp = extracted[i].strip().replace("## ", "").replace(" :", "")
            extracted_text = extracted[i + 1].strip()
            translated_text = translated[i + 1].strip()
            data.append({'timestamp': timestamp,
                         'english': extracted_text,
                         'target_language': translated_text})

    page = request.GET.get('page', 1)
    paginator = Paginator(data, param)
    try:
        paginated_subs = paginator.page(page)
    except PageNotAnInteger:
        paginated_subs = paginator.page(1)
    except EmptyPage:
        paginated_subs = paginator.page(paginator.num_pages)

    return paginated_subs


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
                        transcript_file.write(f"## {entry['start']:.2f} - {(entry['start'] + entry['duration']):.2f}")
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

                # Use TTS API to generate the audio files
                audio_file = tts_convertor(translated_file, target_language, name)
                if target_language == 'French':
                    Video.objects.filter(title=yt.title).update(french_tts_audio_path=audio_file)
                elif target_language == 'German':
                    Video.objects.filter(title=yt.title).update(german_tts_audio_path=audio_file)

                embedded_video = embed_subs_audio(f"media/{name}.mp4", translated_file, audio_file, target_language)
                Video.objects.filter(title=yt.title).update(embedded_video_path=embedded_video)

                return redirect(reverse('download_status', args=[str(name)]))

            except (RegexMatchError, VideoUnavailable, PytubeError, RequestException) as e:
                error_message = str(e)
                return redirect(reverse('download_status', args=[error_message]))
    else:
        form = VideoDownloadForm()

    return render(request, 'downloader.html', {'form': form})


def download_status(request, video_id=None):
    name = "media/" + video_id + ".mp4"
    video = Video.objects.filter(downloaded_video_path=name).first()
    download_success = True if video else False
    download_error = False if video else True
    if download_success:
        paginated_subs = paginate_data(request, str(video.extracted_transcript_path),
                                       str(video.translated_transcript_path), 10)
        video_id = str(video.downloaded_video_path).split('/')[1].split('.')[0]
        context = {
            'download_success': download_success,
            'download_error': download_error,
            'new_filename': video_id,
            'entries_page': paginated_subs,
            'video_id': video_id,
            'video_title': str(video.embedded_video_path).split('/')[1].split('.')[0]
        }
        return render(request, 'download_status.html', context)
    else:
        context = {
            'download_success': download_success,
            'download_error': download_error,
            'new_filename': video_id,
        }
        return render(request, 'download_status.html', context)


def download_subtitle(request, video_id, language):
    name = "media/" + video_id + ".mp4"
    video = Video.objects.filter(downloaded_video_path=name).first()
    if language == 'original':
        subtitle_path = str(video.extracted_transcript_path)
    elif language == 'translated':
        subtitle_path = str(video.translated_transcript_path)
    elif language == 'video':
        response = HttpResponse(open(str(video.embedded_video_path), 'rb').read(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename={video_id}.mp4'
        return response
    else:
        return HttpResponse("Invalid language specified.")

    with open(subtitle_path, 'r', encoding='utf-8') as subtitle_file:
        lines = subtitle_file.readlines()

    subtitles = srt_convertor(lines)

    response = HttpResponse(subtitles, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={language}_subtitles.srt'

    return response


def srt_convertor(lines):
    subtitles = []
    index = 1
    for i in range(0, len(lines)):
        if '##' in lines[i]:
            time_interval = (lines[i].strip().replace(" - ", " --> ")
                             .replace("## ", "").replace(" :", "").replace(":", ""))
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

    return subtitles
