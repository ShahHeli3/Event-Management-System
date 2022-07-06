from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User
from events.models import Testimonials, QuestionAnswerForum, EventCategories, Events, EventIdeas, EventReviews, \
    EventImages


class TestViews(APITestCase):
    """
    class to test views of events app
    """

    def setUp(self):
        self.admin_user = User.objects.create_user(email='admin@gmail.com', username='admin', first_name='Test',
                                                   last_name='Data', password='Abc@1234',
                                                   contact_number='+919876543210', is_event_manager=True)

        self.normal_user = User.objects.create_user(email='heli@gmail.com', username='heli', first_name='Heli',
                                                    last_name='Shah', password='Abc@1234',
                                                    contact_number='+919876543211', is_event_manager=False)

        self.create_testimonial = Testimonials.objects.create(user=self.normal_user, review="Testing")
        self.testimonial_id = self.create_testimonial.id

        self.create_question = QuestionAnswerForum.objects.create(user=self.normal_user, question='Testing QnA')
        self.question_id = self.create_question.id

        self.create_event_category = EventCategories.objects.create(event_category="Test category")
        self.event_category_id = self.create_event_category.id

        self.create_event = Events.objects.create(event_name='Test event', event_details='Test event details',
                                                  event_category=self.create_event_category)
        self.event_id = self.create_event.id

        self.create_event_idea = EventIdeas.objects.create(event=self.create_event, event_idea='Test Idea',
                                                           event_city='Test event city')
        self.event_idea_id = self.create_event_idea.id

    def test_view_testimonials_successful(self):
        """
        function to successfully get testimonials
        """
        response = self.client.get(reverse('view_testimonials'))
        self.assertEqual(response.status_code, 200)

    def test_post_testimonial_fails_if_unauthenticated(self):
        """
        post testimonial fails if user is unauthenticated
        """
        response = self.client.post(reverse('testimonial-list'))
        self.assertEqual(response.status_code, 401)

    def test_post_testimonial_fails_if_no_data(self):
        """
        testimonial cannot be posted if data is not given
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('testimonial-list'))
        self.assertEqual(response.status_code, 400)

    def test_post_testimonial_successful(self):
        """
        post testimonial successful if user is authenticated and valid data is provided
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('testimonial-list'), {'review': 'Test review'}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_testimonial_fails_if_unauthorized_user(self):
        """
        testimonial cannot be updated if the testimonial belongs to some other user
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        testimonial = Testimonials.objects.get(id=self.testimonial_id).id

        response = self.client.put(reverse('testimonial-detail', kwargs={'pk': testimonial}),
                                   {'review': 'Test Update Testimonial'}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_update_testimonial_successful(self):
        """
        testimonial can be updated if authenticated and authorized user is logged in
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        testimonial = Testimonials.objects.get(id=self.testimonial_id).id

        response = self.client.put(reverse('testimonial-detail', kwargs={'pk': testimonial}),
                                   {'review': 'Test Update Testimonial'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_testimonial_fails_if_unauthorized_user(self):
        """
        testimonial cannot be deleted if the testimonial belongs to some other user
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        testimonial = Testimonials.objects.get(id=self.testimonial_id).id

        response = self.client.delete(reverse('testimonial-detail', kwargs={'pk': testimonial}))
        self.assertEqual(response.status_code, 400)

    def test_delete_testimonial_successful(self):
        """
        testimonial can be deleted if authenticated and authorized user is logged in
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        testimonial = Testimonials.objects.get(id=self.testimonial_id).id

        response = self.client.delete(reverse('testimonial-detail', kwargs={'pk': testimonial}),
                                      {'review': 'Test Update Testimonial'}, format='json')
        self.assertEqual(response.status_code, 204)

    def test_cannot_access_question_answers_if_unauthenticated_user(self):
        """
        question and answers cannot be accessed if user is not authenticated
        """
        response = self.client.get(reverse('question_answer'))
        self.assertEqual(response.status_code, 401)

    def test_get_question_answers_successful(self):
        """
        question and answers can be viewed if user is authenticated
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse('question_answer'))
        self.assertEqual(response.status_code, 200)

    def test_add_question_successful(self):
        """
        authenticated user can add a new question
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('add_question'), {'question': 'Test question'}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_add_answer_fails_if_not_admin_user(self):
        """
        unauthorized user cannot add answer to the posted question
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        question = QuestionAnswerForum.objects.get(id=self.question_id).id

        response = self.client.put(reverse('add_answer', kwargs={'id': question}), {'answer': 'Test Answer'},
                                   format='json')
        self.assertEqual(response.status_code, 403)

    def test_add_answer_successful(self):
        """
        only event managers(admin users) can add answer to the posted question
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        question = QuestionAnswerForum.objects.get(id=self.question_id).id

        response = self.client.put(reverse('add_answer', kwargs={'id': question}), {'answer': 'Test Answer'},
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_question_fails_if_not_admin_user(self):
        """
        unauthorized user cannot delete any question
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        question = QuestionAnswerForum.objects.get(id=self.question_id).id

        response = self.client.delete(reverse('add_answer', kwargs={'id': question}))
        self.assertEqual(response.status_code, 403)

    def test_delete_question_successful(self):
        """
        only event managers(admin users) can delete question
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        question = QuestionAnswerForum.objects.get(id=self.question_id).id

        response = self.client.delete(reverse('add_answer', kwargs={'id': question}))
        self.assertEqual(response.status_code, 204)

    def test_view_event_categories_successful(self):
        """
        function to successfully get event categories
        """
        response = self.client.get(reverse('view_event_categories'))
        self.assertEqual(response.status_code, 200)

    def test_post_event_category_fails_if_unauthorized(self):
        """
        unauthorized user cannot post any new event category
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('event_categories-list'), {'event_category': 'Test category'},
                                    format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_event_category_successful(self):
        """
        only event managers(admin users) can add an event category
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse('event_categories-list'), {'event_category': 'Test event category'},
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_event_category_fails_if_unauthorized(self):
        """
        unauthorized user cannot update any new event category
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id

        response = self.client.put(reverse('event_categories-detail', kwargs={'pk': event_category}),
                                   {'event_category': 'Test Update category'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_update_event_category_successful(self):
        """
        only event managers(admin users) can update an event category
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id

        response = self.client.put(reverse('event_categories-detail', kwargs={'pk': event_category}),
                                   {'event_category': 'Test Update category'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_event_category_fails_if_unauthorized(self):
        """
        unauthorized user cannot delete any new event category
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id

        response = self.client.delete(reverse('event_categories-detail', kwargs={'pk': event_category}))
        self.assertEqual(response.status_code, 403)

    def test_delete_event_category_successful(self):
        """
        only event managers(admin users) can delete an event category
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id

        response = self.client.delete(reverse('event_categories-detail', kwargs={'pk': event_category}))
        self.assertEqual(response.status_code, 204)

    def test_view_events_successful(self):
        """
        function to successfully get events
        """
        response = self.client.get(reverse('view_events'))
        self.assertEqual(response.status_code, 200)

    def test_post_event_fails_if_unauthorized(self):
        """
        unauthorized user cannot post any new event
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id

        response = self.client.post(reverse('events-list'), {'event_name': 'Test Event',
                                                             'event_details': 'Test details',
                                                             'event_category': event_category}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_post_event_successful(self):
        """
        only event managers(admin users) can add an event
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id

        response = self.client.post(reverse('events-list'), {'event_name': 'Test Event',
                                                             'event_details': 'Test details',
                                                             'event_category': event_category}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_update_event_fails_if_unauthorized(self):
        """
        unauthorized user cannot update any new event
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id
        event = Events.objects.get(id=self.event_id).id

        response = self.client.put(reverse('events-detail', kwargs={'pk': event}), {'event_name': 'Test Event',
                                                                                    'event_details': 'Test details',
                                                                                    'event_category': event_category},
                                   format='json')
        self.assertEqual(response.status_code, 403)

    def test_update_event_successful(self):
        """
        only event managers(admin users) can update an event
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        event_category = EventCategories.objects.get(id=self.event_category_id).id
        event = Events.objects.get(id=self.event_id).id

        response = self.client.put(reverse('events-detail', kwargs={'pk': event}), {'event_name': 'Test Event',
                                                                                    'event_details': 'Test details',
                                                                                    'event_category': event_category},
                                   format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_event_fails_if_unauthorized(self):
        """
        unauthorized user cannot delete any new event
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event = Events.objects.get(id=self.event_id).id

        response = self.client.delete(reverse('events-detail', kwargs={'pk': event}))
        self.assertEqual(response.status_code, 403)

    def test_delete_event_successful(self):
        """
        only event managers(admin users) can delete an event
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        event = Events.objects.get(id=self.event_id).id

        response = self.client.delete(reverse('events-detail', kwargs={'pk': event}))
        self.assertEqual(response.status_code, 204)

    def test_view_event_ideas_successful(self):
        """
        function to successfully get event ideas
        """
        event = Events.objects.get(id=self.event_id).id

        response = self.client.get(reverse('view_event_ideas', kwargs={'event_id': event}))
        self.assertEqual(response.status_code, 200)

    def test_post_event_idea_fails_if_unauthorized(self):
        """
        unauthorized user cannot post any new event idea
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event = Events.objects.get(id=self.event_id)
        response = self.client.post(reverse('event_ideas-list'),
                                    {'event_id': event.id,
                                     'event_idea': 'Test idea',
                                     'event_city': 'Test City'},
                                    format='json')
        self.assertEqual(response.status_code, 403)

    # def test_post_event_idea_successful(self):
    #     """
    #     only event managers(admin users) can add an event idea
    #     """
    #     user = User.objects.get(username='admin')
    #     self.client.force_authenticate(user=user)
    #
    #     event = Events.objects.get(id=self.event_id).id
    #
    #     response = self.client.post(reverse('event_ideas-list'), {"event_idea": "Hungrito",
    #                                                               "event_city": "Ahmedabad",
    #                                                               "event_id": 20},
    #                                 format='json')
    #     print(response)
    #     self.assertEqual(response.status_code, 201)

    def test_update_event_ideas_fails_if_unauthorized(self):
        """
        unauthorized user cannot update any event idea
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event_idea = EventIdeas.objects.get(id=self.event_idea_id).id
        event = Events.objects.get(id=self.event_id).id

        response = self.client.put(reverse('event_ideas-detail', kwargs={'pk': event_idea}),
                                    {'event_id': event,
                                     'event_idea': 'Test idea',
                                     'event_city': 'Test City'},
                                    format='json')

        self.assertEqual(response.status_code, 403)

    def test_update_event_idea_successful(self):
        """
        only event managers(admin users) can update an event idea
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        event_idea = EventIdeas.objects.get(id=self.event_idea_id).id
        event = Events.objects.get(id=self.event_id).id

        response = self.client.put(reverse('event_ideas-detail', kwargs={'pk': event_idea}),
                                   {'event_id': event,
                                    'event_idea': 'Test idea',
                                    'event_city': 'Test City'},
                                   format='json')

        self.assertEqual(response.status_code, 200)

    def test_delete_event_idea_fails_if_unauthorized(self):
        """
        unauthorized user cannot delete any event idea
        """
        user = User.objects.get(username='heli')
        self.client.force_authenticate(user=user)

        event_idea = EventIdeas.objects.get(id=self.event_idea_id).id

        response = self.client.delete(reverse('event_ideas-detail', kwargs={'pk': event_idea}))
        self.assertEqual(response.status_code, 403)

    def test_delete_event_idea_successful(self):
        """
        only event managers(admin users) can delete an event idea
        """
        user = User.objects.get(username='admin')
        self.client.force_authenticate(user=user)

        event_idea = EventIdeas.objects.get(id=self.event_idea_id).id

        response = self.client.delete(reverse('event_ideas-detail', kwargs={'pk': event_idea}))
        self.assertEqual(response.status_code, 204)
