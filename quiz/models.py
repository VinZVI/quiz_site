import random

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Quiz.Status.PUBLISHED)


class Quiz(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    quiz_title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')  # уникальные slug для даты публикации
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')

    description = models.TextField(blank=False)
    publish = models.DateTimeField('date published', auto_now_add=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              # Post.Status.labels ['Draft', 'Published'] для получения удобочитаемых имен и
                              # Post.Status.values ['DF', 'PB'] чтобы получить фактические значения вариантов
                              default=Status.DRAFT)
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.quiz_title

    def get_absolute_url(self):
        return reverse('quiz:quiz_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)
    maximum_marks = models.DecimalField(_('Maximum Marks'), default=4, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse('quiz:question',
                       args=[self.quiz,
                             self.slug])


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    is_correct = models.BooleanField(_('Is this answer correct?'), default=False, null=False)

    def __str__(self):
        return self.choice_text


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempted_quiz_flag = models.BooleanField(_('Is the attempt over?'), default=True, null=False)

    def __str__(self):
        return f'<QuizProfile: user={self.user}>'

    def create_attempt_quiz(self, quiz, attempt_number):
        attempted_quiz = AttemptedQuiz(quiz=quiz, quiz_profile=self, attempt_number=attempt_number)
        attempted_quiz.save()
        return attempted_quiz

    def get_new_question(self, attempted_quiz):
        used_questions_pk = AttemptedQuestion.objects.filter(quiz_profile=self,
                                                             attempted_quiz=attempted_quiz).values_list('question__pk',
                                                                                                        flat=True)
        remaining_questions = Question.objects.filter(quiz=self.quiz).exclude(pk__in=used_questions_pk)
        if not remaining_questions.exists():
            return
        return random.choice(remaining_questions)

    def create_attempt(self, question, attempted_quiz):
        attempted_question = AttemptedQuestion(question=question, quiz_profile=self, attempted_quiz=attempted_quiz)
        attempted_question.save()

    def evaluate_attempt(self, attempted_question, selected_choice):
        if attempted_question.question_id != selected_choice.question_id:
            return

        attempted_question.selected_choice = selected_choice
        if selected_choice.is_correct is True:
            attempted_question.is_correct = True
            attempted_question.marks_obtained = attempted_question.question.maximum_marks

        attempted_question.save()
        self.update_score()

    def update_score(self):
        marks_sum = self.attempts.filter(is_correct=True).aggregate(
            models.Sum('marks_obtained'))['marks_obtained__sum']
        self.total_score = marks_sum or 0
        self.save()


class AttemptedQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    quiz_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='attempts_quiz')
    date_of_birth = models.DateField(auto_now_add=True, blank=True, null=True)
    total_score = models.DecimalField(_('Total Score'), default=0, decimal_places=2, max_digits=10)
    attempt_number = models.PositiveIntegerField(_('Number Attempt'), default=0, null=False)

    def get_absolute_url(self):
        return f'/submission-result/{self.pk}/'


class AttemptedQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    quiz_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='attempts')
    attempted_quiz = models.ForeignKey(AttemptedQuiz, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    is_correct = models.BooleanField(_('Was this attempt correct?'), default=False, null=False)
    marks_obtained = models.DecimalField(_('Marks Obtained'), default=0, decimal_places=2, max_digits=6)

    def get_absolute_url(self):
        return f'/submission-result/{self.pk}/'
