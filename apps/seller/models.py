from django.db import models

class SellerProfile(models.Model):
    store_name = models.CharField(max_length=150, blank=True)
    tagline = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        verbose_name = 'SellerProfile'
        verbose_name_plural = 'SellerProfiles'
