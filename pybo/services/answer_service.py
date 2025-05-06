
from django.utils import timezone
from django.shortcuts import get_object_or_404
from pybo.models import Answer, Question

class AnswerService:
    @staticmethod
    def create_answer(user, question_id, form):
        if not form.is_valid():
            raise ValueError("Invalid form data")
        question = get_object_or_404(Question, pk=question_id)
        answer = form.save(commit=False)
        answer.author = user
        answer.create_date = timezone.now()
        answer.question = question
        answer.save()
        return answer

    @staticmethod
    def modify_answer(answer, form):
        if not form.is_valid():
            raise ValueError("Invalid form data")
        answer = form.save(commit=False)
        answer.modify_date = timezone.now()
        answer.save()
        return answer

    @staticmethod
    def delete_answer(answer):
        answer.delete()
