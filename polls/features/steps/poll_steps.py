import datetime

from behave import given, then, when
from polls.models import Question
from django.urls import reverse
from django.utils import timezone


@given(u'A question {question_name} with text {question_text}')
def question_create(context, question_name, question_text):
    question = Question.objects.create(question_text=question_text,
                                       pub_date=timezone.now())
    context.questions[question_name] = question


@given(u'{question_name} has publish date set to {num_days} days {direction} today')
def step_impl(context, question_name, num_days, direction):
    question = context.questions[question_name]
    if direction == 'from':
        question.pub_date = timezone.now() + datetime.timedelta(days=int(num_days))
    elif direction == 'before':
        question.pub_date = timezone.now() - datetime.timedelta(days=int(num_days))
    else:
        raise NotImplementedError('Unknown direction ', direction)
    question.save()

@when(u'user visits the detail page for {question_name}')
def step_impl(context, question_name):
    question = context.questions[question_name]
    url = reverse('polls:detail', args=(question.id,))
    context.response = context.test.client.get(url)

@then(u'user get a page not found error')
def step_impl(context):
    context.test.assertEqual(context.response.status_code, 404)


@then(u'user gets to see the details of {question_name}')
def step_impl(context, question_name):
    question = context.questions[question_name]
    context.test.assertContains(context.response, question.question_text)
