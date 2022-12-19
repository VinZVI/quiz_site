from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)
    #photo = models.ImageField(upload_to='users/%Y/%m/%d/',
    #                          blank=True)


def __str__(self):
    return f'Profile of {self.user.username}'

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Quiz.Status.PUBLISHED)
class Quiz(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    quiz_title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    description = models.TextField()
    publish = models.DateTimeField('date published', auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices, # Post.Status.labels ['Draft', 'Published'] для получения удобочитаемых имен и
                                                      # Post.Status.values ['DF', 'PB'] чтобы получить фактические значения вариантов
                              default=Status.DRAFT)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.quiz_title

    # def get_questions(self):
    #     return self.question_set.all()

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)


    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)

    def __str__(self):
        return self.choice_text
