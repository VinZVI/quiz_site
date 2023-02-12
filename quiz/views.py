from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from .forms import LoginForm
from .forms import RegistrationForm
from .models import Quiz, Profile, AttemptedQuestion, AttemptedQuiz


def home(request):
    context = {}
    return render(request, 'quiz/home.xhtml', context=context)


@login_required()
def choose_of_quizzes(request):
    quiz_list = Quiz.published.all()
    context = {
        'quiz_list': quiz_list,
    }
    return render(request, 'quiz/choose_of_quizzes.xhtml', context=context)

def quiz_detail(request, year, month, day, slug):

    quiz = get_object_or_404(Quiz,
                             status=Quiz.Status.PUBLISHED,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)


    return render(request, 'quiz/quiz_detail.xhtml',
                  {'quiz': quiz})


@login_required()
def play(request, year, month, day, slug):
    quiz = get_object_or_404(Quiz,
                             status=Quiz.Status.PUBLISHED,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    quiz_profile, created = Profile.objects.get_or_create(user=request.user, quiz=quiz, )

    if created:
        quiz_profile.create_attempt_quiz(quiz, 1)
        quiz_profile.attempted_quiz_flag = False
        quiz_profile.save()
    try:
        last_attempt_quiz = quiz_profile.attempts_quiz.latest('attempt_number')
        last_attempt_number = last_attempt_quiz.attempt_number  # last_attempt_number[0][0]
    except:
        quiz_profile.create_attempt_quiz(quiz, 1)
        quiz_profile.attempted_quiz_flag = False
        last_attempt_number = quiz_profile.attempts_quiz.reverse().values_list('attempt_number')

    if quiz_profile.attempted_quiz_flag:
        last_attempt_number += 1
        last_attempt_quiz = quiz_profile.create_attempt_quiz(quiz, last_attempt_number)
        quiz_profile.attempted_quiz_flag = False
        quiz_profile.save()

    if request.method == 'POST':
        question_pk = request.POST.get('question_pk')

        attempted_question = quiz_profile.attempts.filter(attempted_quiz=last_attempt_quiz).select_related(
            'question').get(question__pk=question_pk)

        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = attempted_question.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

        quiz_profile.evaluate_attempt(attempted_question, selected_choice)

        return redirect(attempted_question)

    else:
        question = quiz_profile.get_new_question(last_attempt_quiz)
        if question is not None:
            quiz_profile.create_attempt(question, last_attempt_quiz)
        else:
            quiz_profile.attempted_quiz_flag = True
            # attempted_quiz = AttemptedQuiz.objects.filter(quiz_profile=quiz_profile, attempted_quiz=last_attempt_quiz).get()

            last_attempt_quiz.total_score = quiz_profile.total_score
            quiz_profile.total_score = 0
            quiz_profile.save()
            last_attempt_quiz.save()

        context = {
            'question': question,
            'used_quiz': quiz
        }

        return render(request, 'quiz/play.xhtml', context=context)


@login_required()
def submission_result(request, attempted_question_pk):
    attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    use_quiz = attempted_question.quiz_profile.quiz

    context = {
        'quiz': use_quiz,
        'attempted_question': attempted_question,
    }

    return render(request, 'quiz/submission_result.xhtml', context=context)


def user_login(request):
    title = "Login"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                    return redirect('/choose_of_quizzes')
                    # return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'quiz/login.xhtml', {'form': form, "title": title})


def leaderboard(request, year, month, day, slug):
    used_quiz = get_object_or_404(Quiz,
                                  status=Quiz.Status.PUBLISHED,
                                  slug=slug,
                                  publish__year=year,
                                  publish__month=month,
                                  publish__day=day)
    top_attempted_quiz = AttemptedQuiz.objects.filter(quiz=used_quiz).order_by('-total_score')[:500]
    total_count = top_attempted_quiz.count()
    context = {
        'top_attempted_quiz': top_attempted_quiz,
        'total_count': total_count,
        'used_quiz': used_quiz,
    }
    return render(request, 'quiz/leaderboard.xhtml', context=context)





# def login_view(request):
#     title = "Login"
#     form = UserLoginForm(request.POST or None)
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         return redirect('/user-home')
#     return render(request, 'quiz/login.html', {"form": form, "title": title})


def register(request):
    title = "Create account"
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = RegistrationForm()

    context = {'form': form, 'title': title}
    return render(request, 'quiz/registration.xhtml', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


def error_404(request):
    data = {}
    return render(request, 'quiz/error_404.xhtml', data)


def error_500(request):
    data = {}
    return render(request, 'quiz/error_500.xhtml', data)
