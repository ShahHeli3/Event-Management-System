from rest_framework.test import APISimpleTestCase
from django.urls import reverse, resolve

from events.views import ViewTestimonials, TestimonialsViewSet, QuestionAnswersView, AddQuestionView, AddAnswerView, \
    GetEventCategoriesView, EventCategoriesViewSet, GetEventsView, EventsViewSet, GetEventIdeasView, EventIdeasViewSet, \
    EventImagesViewSet, EventReviewViewSet


class TestUrls(APISimpleTestCase):
    """
    class to test all the urls of events app
    """

    def check_urls(self, url, view):
        """
        function to test if the given url matches with its view
        :param url: url to be tested
        :param view: view connected to the url
        """
        self.assertEqual(resolve(url).func.view_class, view)

    def check_routers(self, router, viewset):
        """
        function to test if the given router matches with its viewset
        :param router: url to be tested
        :param viewset: viewset connected to the url
        """
        self.assertEqual(resolve(router).func.cls, viewset)

    # testing routers
    def test_testimonial_view_set_list_router(self):
        """
        function to test if the testimonial post router works
        """
        self.check_routers(reverse('testimonial-list'), TestimonialsViewSet)

    def test_testimonial_view_set_detail_router(self):
        """
        function to test if the testimonial put and delete router works
        """
        self.check_routers(reverse('testimonial-detail', kwargs={'pk': 1}), TestimonialsViewSet)

    def test_event_categories_view_set_list_router(self):
        """
        function to test if the event categories post router works
        """
        self.check_routers(reverse('event_categories-list'), EventCategoriesViewSet)

    def test_event_categories_view_set_detail_router(self):
        """
        function to test if the event categories put and delete router works
        """
        self.check_routers(reverse('event_categories-detail', kwargs={'pk': 1}), EventCategoriesViewSet)

    def test_events_view_set_list_router(self):
        """
        function to test if the events create/post router works
        """
        self.check_routers(reverse('events-list'), EventsViewSet)

    def test_events_view_set_detail_router(self):
        """
        function to test if the events put and delete router works
        """
        self.check_routers(reverse('events-detail', kwargs={'pk': 1}), EventsViewSet)

    def test_event_ideas_view_set_list_router(self):
        """
        function to test if the event ideas router works
        """
        self.check_routers(reverse('event_ideas-list'), EventIdeasViewSet)

    def test_event_ideas_view_set_detail_router(self):
        """
        function to test if the event ideas put and delete router works
        """
        self.check_routers(reverse('event_ideas-detail', kwargs={'pk': 1}), EventIdeasViewSet)

    def test_event_images_view_set_list_router(self):
        """
        function to test if the event images router works
        """
        self.check_routers(reverse('event_images-list'), EventImagesViewSet)

    def test_event_images_view_set_detail_router(self):
        """
        function to test if the event images put and delete router works
        """
        self.check_routers(reverse('event_images-detail', kwargs={'pk': 1}), EventImagesViewSet)

    def test_event_reviews_view_set_list_router(self):
        """
        function to test if the event reviews router works
        """
        self.check_routers(reverse('event_reviews-list'), EventReviewViewSet)

    def test_event_reviews_view_set_detail_router(self):
        """
        function to test if the event reviews put and delete router works
        """
        self.check_routers(reverse('event_reviews-detail', kwargs={'pk': 1}), EventReviewViewSet)

    # testing urls
    def test_view_testimonials_url(self):
        """
        function to test if the view_testimonials url works
        """
        self.check_urls(reverse('view_testimonials'), ViewTestimonials)

    def test_question_answer_url(self):
        """
        function to test if the question_answer url works
        """
        self.check_urls(reverse('question_answer'), QuestionAnswersView)

    def test_add_question_url(self):
        """
        function to test if the add_question url works
        """
        self.check_urls(reverse('add_question'), AddQuestionView)

    def test_add_answer_url(self):
        """
        function to test if the add_answer url works
        """
        self.check_urls(reverse('add_answer', kwargs={'id': 1}), AddAnswerView)

    def test_view_event_categories_url(self):
        """
        function to test if the view_event_categories url works
        """
        self.check_urls(reverse('view_event_categories'), GetEventCategoriesView)

    def test_view_events_url(self):
        """
        function to test if the view_testimonials url works
        """
        self.check_urls(reverse('view_events'), GetEventsView)

    def test_view_event_ideas_url(self):
        """
        function to test if the view_event_ideas url works
        """
        self.check_urls(reverse('view_event_ideas', kwargs={'event_id': 1}), GetEventIdeasView)
