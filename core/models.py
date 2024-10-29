from django.db import models
from user.models import Profile

class NoteCategory(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ["title"]

    def __str__(self):
        return self.title


class Note(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(NoteCategory,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='category_notes'
                                 )
    profile = models.ForeignKey(Profile,
                                related_name='profile_notes',
                                on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ["-created_date"]

    def __str__(self):
        return self.title


class NoteComment(models.Model):
    text = models.TextField(max_length=1000)
    note = models.ForeignKey(Note,
                             on_delete=models.CASCADE,
                             related_name='note_comments'
                             )
    profile = models.ForeignKey(Profile,
                                related_name='profile_comments',
                                on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ["-id"]

    def __str__(self):
        return self.text[:10]


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return self.name

class Favorites(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_followers')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                related_name='profile_following')
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('author', 'note')

    def __str__(self):
        return self.profile.user.username