from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from garpix_page.models import BasePage
from blog.utils import get_file_path
from blog.models import BlogPage


def get_display(key, _list):
    d = dict(_list)
    if key in d:
        return d[key]
    return None


class PostPage(BasePage):
    class TYPE:
        NEW = 1
        PROMOTION = 2

        CHOICES = (
            (NEW, "Новость"),
            (PROMOTION, "Акция")
        )

    blog = models.ForeignKey(BlogPage, verbose_name='Родительская страница', blank=True, null=True,
                             on_delete=models.SET_NULL, db_index=True)
    short_description = models.CharField(verbose_name='Краткое описание', max_length=1000, blank=True)
    news_content = RichTextUploadingField(blank=True, null=True, verbose_name='Контент новости')
    image_preview = models.ImageField(verbose_name="Изображение превью", blank=True, null=True, upload_to=get_file_path)
    type = models.IntegerField(default=TYPE.NEW, choices=TYPE.CHOICES, verbose_name='Новость/Акция?')

    def __str__(self):
        return f'{self.get_choice_verbose()} {self.title}'

    def get_choice_verbose(self):
        return get_display(self.type, self.TYPE.CHOICES)

    class Meta:
        verbose_name = "Новость/Акция"
        verbose_name_plural = "Новости/Акции"
        ordering = ('-created_at',)
