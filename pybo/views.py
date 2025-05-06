
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer
from .services.question_service import QuestionService
from .services.answer_service import AnswerService


def index(request):
    page = request.GET.get('page', '1')
    question_list = QuestionService.get_paginated_questions(page)
    return render(request, 'pybo/question_list.html', {'question_list': question_list})


def detail(request, question_id):
    question = QuestionService.get_question_by_id(question_id)
    return render(request, 'pybo/question_detail.html', {'question': question})


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        try:
            question = QuestionService.create_question(request.user, form)
            return redirect('pybo:detail', question_id=question.id)
        except Exception as e:
            messages.error(request, str(e))
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        raise PermissionDenied
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        try:
            QuestionService.modify_question(question, form)
            return redirect('pybo:detail', question_id=question.id)
        except Exception as e:
            messages.error(request, str(e))
    else:
        form = QuestionForm(instance=question)
    return render(request, 'pybo/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        raise PermissionDenied
    QuestionService.delete_question(question)
    return redirect('pybo:index')


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = QuestionService.get_question_by_id(question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        try:
            AnswerService.create_answer(request.user, question_id, form)
            return redirect('pybo:detail', question_id=question_id)
        except Exception as e:
            messages.error(request, str(e))
    else:
        form = AnswerForm()
    return render(request, 'pybo/question_detail.html', {'question': question, 'form': form})


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        raise PermissionDenied
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        try:
            AnswerService.modify_answer(answer, form)
            return redirect('pybo:detail', question_id=answer.question.id)
        except Exception as e:
            messages.error(request, str(e))
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'pybo/answer_form.html', {'form': form})


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        raise PermissionDenied
    AnswerService.delete_answer(answer)
    return redirect('pybo:detail', question_id=answer.question.id)
