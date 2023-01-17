from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Question, Choice, File, Quiz


class LoginForm(forms.Form):
    username = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            # 'password1',
            # 'password2',
        ]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class FileEditForm(forms.ModelForm):
    # quiz = forms.CharField()
    file = forms.FileField()

    # owner = forms.CharField()
    class Meta:
        model = File
        fields = ['file']

    # def save(self, quiz, user):
    #     self.quiz = quiz
    #     self.owner = user
    #     super(FileEditForm, self).save()


class QuizForm(forms.ModelForm):
    # author = forms.CharField(disabled=True)
    quiz_title = forms.CharField(required=True)
    description = forms.CharField(required=True)
    slug = forms.SlugField(disabled=True)

    class Meta:
        model = Quiz
        fields = ['quiz_title', 'slug', 'description', 'status']


from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet

ChoiceFormset = inlineformset_factory(Question,
                                      Choice,
                                      fields=('choice_text',
                                              'is_correct',),
                                      extra=4,
                                      max_num=4)


class BaseQuestionFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseQuestionFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = ChoiceFormset(
            instance=form.instance,
            # data=form.data if form.is_bound else None,)
            # files=form.files if form.is_bound else None,
            prefix='choice-%s-%s' % (
                form.prefix,
                ChoiceFormset.get_default_prefix()))
        # extra=4)

    def is_valid(self):
        result = super(BaseQuestionFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

    def save(self, commit=True):

        result = super(BaseQuestionFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


QuestionFormset = inlineformset_factory(Quiz, Question,
                                        formset=BaseQuestionFormset,
                                        fields=('question_text', 'description', 'maximum_marks',),
                                        extra=3,
                                        max_num=2)

# class QuestionForm(forms.ModelForm):
#     class Meta:
#         model = Question
#         fields = ['quiz', 'question_text', 'description']
#         widgets = {
#             'question_text': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
#         }
#
#
# class ChoiceForm(forms.ModelForm):
#     class Meta:
#         model = Choice
#         fields = ['choice_text', 'is_correct']
#         widgets = {
#             'html': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
#         }


# class ChoiceInlineFormset(forms.BaseInlineFormSet):
#     def clean(self):
#         super(ChoiceInlineFormset, self).clean()
#
#         correct_choices_count = 0
#         for form in self.forms:
#             if not form.is_valid():
#                 return
#
#             if form.cleaned_data and form.cleaned_data.get('is_correct') is True:
#                 correct_choices_count += 1

# try:
#     assert correct_choices_count == Question.ALLOWED_NUMBER_OF_CORRECT_CHOICES
# except AssertionError:
#     raise forms.ValidationError(_('Exactly one correct choice is allowed.'))
