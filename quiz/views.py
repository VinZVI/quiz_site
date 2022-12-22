from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.decorators import login_required

from .models import Question, Choice, Quiz, Profile


def home(request):

    context = {}
    return render(request, 'quiz/home.xhtml', context=context)


@login_required()
def user_home(request):
    quiz_list = Quiz.published.all()
    context = {
        'quiz_list': quiz_list,
    }
    return render(request, 'quiz/user_home.xhtml', context=context)

def quiz_detail(request, year, month, day, slug):
    # quiz = get_object_or_404(Quiz,
    #                          id=id,
    #                          status=Quiz.Status.PUBLISHED)

    quiz = get_object_or_404(Quiz,
                             status=Quiz.Status.PUBLISHED,
                             slug=slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)


    return render(request, 'quiz/quiz_detail.xhtml',
                  {'quiz': quiz})

@login_required()
def play(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    #question = Question.objects.get(id=question_id)
    quiz_profile, created = Profile.objects.get_or_create(user=request.user, quiz=quiz,)
    if request.method == 'POST':

        question_pk = request.POST.get('question_pk')

        #use_question = quiz_profile.question

        choice_pk = request.POST.get('choice_pk')

        try:
            selected_choice = quiz_profile.question.choices.get(pk=choice_pk)
        except ObjectDoesNotExist:
            raise Http404

        quiz_profile.evaluate_attempt(quiz_profile, selected_choice)

        return redirect(quiz_profile, quiz_id=quiz_id)

    else:
        question = quiz.get_question()
        if question is not None:
            quiz_profile.create_attempt(question)

        context = {
            'question': question,
        }

        return render(request, 'quiz/play.xhtml', context=context)



def user_login(request):
    title = "Login"
    if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    user = User.objects.get(username=cd['username'])
                except User.DoesNotExist:
                    user = None
                # user = authenticate(request,
                #                     username=cd['username'],
                #                     password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
                        return redirect('/user-home')
                        #return HttpResponse('Authenticated successfully')
                    else:
                        return HttpResponse('Disabled account')
                else:
                    return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'quiz/login.xhtml', {'form': form, "title": title})

def leaderboard(request):

    top_quiz_profiles = Profile.objects.order_by('-total_score')[:500]
    total_count = top_quiz_profiles.count()
    context = {
        'top_quiz_profiles': top_quiz_profiles,
        'total_count': total_count,
    }
    return render(request, 'quiz/leaderboard.html', context=context)


# @login_required()
# def play(request):
#     quiz_profile, created = Profile.objects.get_or_create(user=request.user)
#
#     if request.method == 'POST':
#         question_pk = request.POST.get('question_pk')
#
#         attempted_question = quiz_profile.attempts.select_related('question').get(question__pk=question_pk)
#
#         choice_pk = request.POST.get('choice_pk')
#
#         try:
#             selected_choice = attempted_question.question.choices.get(pk=choice_pk)
#         except ObjectDoesNotExist:
#             raise Http404
#
#         quiz_profile.evaluate_attempt(attempted_question, selected_choice)
#
#         return redirect(attempted_question)
#
#     else:
#         question = quiz_profile.get_new_question()
#         if question is not None:
#             quiz_profile.create_attempt(question)
#
#         context = {
#             'question': question,
#         }
#
#         return render(request, 'quiz/play.html', context=context)


@login_required()
def submission_result(request, attempted_question_pk):
    # attempted_question = get_object_or_404(AttemptedQuestion, pk=attempted_question_pk)
    # context = {
    #     'attempted_question': attempted_question,
    # }

    return render(request, 'quiz/submission_result.html',) #context=context)


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
    # if request.method == 'POST':
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/login')
    # else:
    #     form = RegistrationForm()

    # context = {'form': form, 'title': title}
    # return render(request, 'quiz/registration.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')


def error_404(request):
    data = {}
    return render(request, 'quiz/error_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'quiz/error_500.html', data)



