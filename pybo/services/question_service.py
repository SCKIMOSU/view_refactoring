
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.utils import timezone
from pybo.models import Question

class QuestionService:
    @staticmethod
    def get_paginated_questions(page, per_page=10):
        question_list = Question.objects.order_by('-create_date')
        paginator = Paginator(question_list, per_page)
        return paginator.get_page(page)

    @staticmethod
    def get_question_by_id(question_id):
        return get_object_or_404(Question, pk=question_id)

    @staticmethod
    def create_question(user, form):
        if not form.is_valid():
            raise ValueError("Invalid form data")
        question = form.save(commit=False)
        question.author = user
        question.create_date = timezone.now()
        question.save()
        return question

    @staticmethod
    def modify_question(question, form):
        if not form.is_valid():
            raise ValueError("Invalid form data")
        question = form.save(commit=False)
        question.modify_date = timezone.now()
        question.save()
        return question

    @staticmethod
    def delete_question(question):
        question.delete()
