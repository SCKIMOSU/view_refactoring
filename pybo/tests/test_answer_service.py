import pytest
from django.contrib.auth.models import User
from pybo.models import Question
from pybo.forms import AnswerForm
from pybo.services.answer_service import AnswerService
from django.utils.timezone import now


@pytest.mark.django_db
def test_create_answer_valid():
    user = User.objects.create_user(username='tester', password='pass')
    question = Question.objects.create(
        subject="test",
        content="content",
        author=user,
        create_date=now()   # 🛠️ create_date 명시
    )

    form_data = {'content': 'test answer'}
    form = AnswerForm(data=form_data)

    answer = AnswerService.create_answer(user, question.id, form)

    assert answer.content == 'test answer'
    assert answer.author == user
    assert answer.question == question
