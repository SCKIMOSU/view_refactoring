
import pytest
from django.contrib.auth.models import User
from pybo.models import Question
from pybo.services.question_service import QuestionService
from django.utils.timezone import now

@pytest.mark.django_db
def test_get_paginated_questions():
    user = User.objects.create_user(username='tester', password='pass')
    for i in range(15):
        Question.objects.create(subject=f"q{i}",
                                content="내용",
                                author=user,
                                create_date=now()   # ← 이 줄 추가!
                                )

    page = QuestionService.get_paginated_questions(page=1)
    assert len(page.object_list) == 10

@pytest.mark.django_db
def test_get_question_by_id():
    user = User.objects.create_user(username='tester', password='pass')
    question = Question.objects.create(
        subject="test",
        content="내용",
        author=user,
        create_date=now()  # ← 이 줄 추가!
    )
    found = QuestionService.get_question_by_id(question.id)
    assert found.subject == "test"
    assert found.author.username == "tester"
    assert found.author.check_password("pass")
    assert found.content == "내용"
    assert found.author == user

