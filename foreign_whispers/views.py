from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import VideoDownloadForm
from pytube import YouTube
import os


def download_video(request):
    if request.method == 'POST':
        form = VideoDownloadForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            try:
                yt = YouTube(video_url)
                video_stream = yt.streams.get_highest_resolution()

                # Name of the video
                video_name = yt.title
                video_name = video_name.replace(' ', '_').split(':')[0]

                # Make it a valid windows directory name
                invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
                for char in invalid_chars:
                    video_name = video_name.replace(char, '')

                # Define the download directory (media root)
                media_root = 'media/'

                # Check if the video is already downloaded
                if f'{video_name}.mp4' in os.listdir(media_root):
                    messages.info(request, f'Video {video_name} already downloaded')
                else:
                    # Download video
                    video_stream.download(output_path=os.path.join(media_root, video_name))

                    # Download captions
                    captions = yt.captions.all()
                    for caption in captions:
                        caption.download(
                            output_path=os.path.join(media_root, video_name),
                            srt=True,
                            title=video_name
                        )

                    # Process the downloaded video using neural networks here
                    messages.success(request, 'Video downloaded successfully.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
            return redirect('download_video')
    else:
        form = VideoDownloadForm()
    return render(request, 'downloader.html', {'form': form})
