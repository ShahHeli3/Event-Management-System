from rest_framework.test import APITestCase

from accounts.models import User
from events.models import Testimonials, QuestionAnswerForum, EventCategories, Events, EventIdeas, EventReviews, \
    EventImages


class TestModels(APITestCase):
    """
    for testing models of events app
    """

    def setUp(self):
        self.user = User.objects.create(email='heli@gmail.com', username='heli', first_name='Heli', last_name='Shah',
                                        contact_number='+919876543210', is_event_manager=True)
        # for testimonial model
        self.review = 'Test Review'

        # for qna model
        self.question = 'Test Question'
        self.answer = 'Test Answer'

        # for event category model
        self.event_category = 'Test Category'

        # for events model
        self.event_name = 'Test Event'
        self.event_details = 'Test event details'

        # for event ideas model
        self.event_idea = 'Test Event Idea'
        self.event_city = 'Test Event City'

        # for event images model
        self.event_image_title = 'Test Image Title'
        self.event_image_details = 'Test image details'
        # self.event_image = SimpleUploadedFile(name='test.jpg', content=open('media/default.jpg', 'rb').read(),
        #                                     content_type='image/jpg')

        # for event reviews model
        self.event_review = 'Test Event Review'

        self.create_testimonial = Testimonials.objects.create(user=self.user, review=self.review)
        self.create_qna = QuestionAnswerForum.objects.create(user=self.user, question=self.question, answer=self.answer)
        self.create_event_category = EventCategories.objects.create(event_category=self.event_category)
        self.create_event = Events.objects.create(event_name=self.event_name, event_details=self.event_details,
                                                  event_category=self.create_event_category)
        self.create_event_idea = EventIdeas.objects.create(event=self.create_event, event_idea=self.event_idea,
                                                           event_city=self.event_city)
        self.create_event_review = EventReviews.objects.create(event_idea=self.create_event_idea, user=self.user,
                                                               event_review=self.event_review)

        with open('media/default.jpg') as fp:
            self.event_image = fp.name

        self.create_event_image = EventImages.objects.create(event_idea=self.create_event_idea,
                                                             event_image=self.event_image,
                                                             event_image_title=self.event_image_title,
                                                             event_image_details=self.event_image_details)

    def test_testimonial_model(self):
        """
        function to test if the testimonial model functions correctly
        """
        self.assertEqual(self.create_testimonial.user, self.user)
        self.assertEqual(self.create_testimonial.review, self.review)

    def test_question_answer_forum_model(self):
        """
        function to test if the question and answers model functions correctly
        """
        self.assertEqual(self.create_qna.user, self.user)
        self.assertEqual(self.create_qna.question, self.question)
        self.assertEqual(self.create_qna.answer, self.answer)

    def test_event_category_model(self):
        """
        function to test if the event categories model functions correctly
        """
        self.assertEqual(self.create_event_category.event_category, self.event_category)

    def test_events_model(self):
        """
        function to test if the events model functions correctly
        """
        self.assertEqual(self.create_event.event_name, self.event_name)
        self.assertEqual(self.create_event.event_details, self.event_details)
        self.assertEqual(self.create_event.event_category, self.create_event_category)

    def test_event_ideas_model(self):
        """
        function to test if the event ideas model functions correctly
        """
        self.assertEqual(self.create_event_idea.event, self.create_event)
        self.assertEqual(self.create_event_idea.event_idea, self.event_idea)
        self.assertEqual(self.create_event_idea.event_city, self.event_city)

    def test_event_reviews_model(self):
        """
        function to test if the event ideas model functions correctly
        """
        self.assertEqual(self.create_event_review.event_idea, self.create_event_idea)
        self.assertEqual(self.create_event_review.user, self.user)
        self.assertEqual(self.create_event_review.event_review, self.event_review)

    def test_event_images_model(self):
        """
        function to test if the event images model functions correctly
        """
        self.assertEqual(self.create_event_image.event_idea, self.create_event_idea)
        self.assertEqual(self.create_event_image.event_image, self.event_image)
        self.assertEqual(self.create_event_image.event_image_title, self.event_image_title)
        self.assertEqual(self.create_event_image.event_image_details, self.event_image_details)
