from django.db import models


class HomeSliderImage(models.Model):
    cover = models.ImageField(upload_to='home_slider_images')
    cover_link = models.TextField(blank=True)
    cover_title = models.CharField(max_length=128, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cover_title