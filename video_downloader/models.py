from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=200)
    video_url = models.URLField()
    downloaded_video_path = models.FileField(upload_to='videos/')
    downloaded_transcript_path = models.FileField(upload_to='transcripts/', null=True, blank=True)
    extracted_audio_path = models.FileField(upload_to='audios/', null=True, blank=True)
    extracted_transcript_path = models.FileField(upload_to='extracts/', null=True, blank=True)
    translated_transcript_path = models.FileField(upload_to='translated/', null=True, blank=True)
    tts_audio_path = models.FileField(upload_to='tts/', null=True, blank=True)

    class Meta:
        app_label = 'video_downloader'
