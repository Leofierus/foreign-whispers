from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    downloaded_video_path = models.FileField(upload_to='videos/')
    downloaded_captions_path = models.FileField(upload_to='captions/', null=True, blank=True)
    downloaded_transcript_path = models.FileField(upload_to='transcripts/', null=True, blank=True)

    class Meta:
        app_label = 'video_downloader'
