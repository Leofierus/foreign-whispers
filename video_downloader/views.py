from django.shortcuts import render
from requests import RequestException

from .forms import VideoDownloadForm
from .models import Video
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable, PytubeError
from youtube_transcript_api import YouTubeTranscriptApi


def download_video(request):
    if request.method == 'POST':
        form = VideoDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']

            try:
                yt = YouTube(video_url)
                video = yt.streams.get_highest_resolution()
                name = yt.video_id
                video.download(filename='media/' + name + '.mp4')

                captions = yt.captions.get_by_language_code('en')
                captions_filename = f"{name}_captions.srt"
                transcript_filename = f"{name}_transcript.txt"

                if captions:
                    captions_content = captions.generate_srt_captions()
                    captions_file_path = "media/"+captions_filename

                    with open(captions_file_path, 'w', encoding='utf-8') as captions_file:
                        captions_file.write(captions_content)
                else:
                    transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)
                    transcript_file_path = "media/"+transcript_filename

                    with open(transcript_file_path, 'w', encoding='utf-8') as transcript_file:
                        for entry in transcript:
                            transcript_file.write(f"{entry['start']} --> {entry['start'] + entry['duration']}\n")
                            transcript_file.write(f"{entry['text']}\n\n")

                # Create a new Video object in the database
                Video.objects.create(
                    title=yt.title,
                    video_url=video_url,
                    downloaded_video_path=f"media/{name}.mp4",
                    downloaded_captions_path=f"media/{captions_filename}" if captions else None,
                    downloaded_transcript_path=f"media/{transcript_filename}" if not captions else None
                )

                return download_status(request, True, None, name)

            except (RegexMatchError, VideoUnavailable, PytubeError, RequestException) as e:
                error_message = str(e)
                return download_status(request, False, error_message)

    else:
        form = VideoDownloadForm()

    return render(request, 'downloader.html', {'form': form})


def download_status(request, download_success, download_error=None, new_filename=None):
    context = {
        'download_success': download_success,
        'download_error': download_error,
        'new_filename': new_filename,
    }
    return render(request, 'download_status.html', context)
