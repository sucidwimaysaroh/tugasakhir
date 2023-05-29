from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .utils import contrastStretching, glcm, Node, DecisionTree, RandomForest
from PIL import Image
from io import BytesIO
import numpy as np
import skimage
import pickle
from django.core.files.base import ContentFile

hasil_classify = (
    ('0', 'Normal'),
    ('1', 'Abnormal')
    )

class Classify(models.Model):
    nama_Dokter = models.ForeignKey(User, on_delete=models.CASCADE)
    nama_Pasien = models.CharField(max_length=100)
    tanggal_Lahir = models.DateField()
    nomer_Rekam_Medis = models.CharField(max_length=100)
    gambar_Mammogram = models.ImageField(upload_to='raw_mammogram')
    gambar_Mammogram_Contrast_Stretching = models.ImageField(upload_to='cs_mammogram')
    fitur = models.TextField()
    hasil = models.CharField(choices=hasil_classify, max_length=1)
    tanggal_Skrining = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('classify-hasil', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        new_image_name = self.gambar_Mammogram.name.split("/")[-1]
        image = skimage.img_as_ubyte(skimage.io.imread(self.gambar_Mammogram, as_gray=True))
        image_cs = contrastStretching(image)
        image_glcm = glcm(image_cs)

        model = pickle.load(open('model.pkl', 'rb'))
        image_rf = model.predict([image_glcm])

        cs = skimage.io.imsave('media/cs_mammogram/'+new_image_name, image_cs)
        self.gambar_Mammogram_Contrast_Stretching = 'cs_mammogram/'+new_image_name
        self.fitur = image_glcm
        self.hasil = image_rf
        return super().save(*args, **kwargs)

