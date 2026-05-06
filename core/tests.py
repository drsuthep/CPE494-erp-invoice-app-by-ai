import re
from django.test import TestCase
from django.urls import reverse

class LandingPageTests(TestCase):
    """
    Tests for the landing page view as specified in Sprint 0.
    """

    def test_landing_returns_200(self):
        """
        Test Case: test_landing_returns_200
        Verifies that a GET request to the root URL returns a 200 OK status.
        """
        response = self.client.get(reverse('core:landing'))
        self.assertEqual(response.status_code, 200)

    def test_landing_contains_hello_world(self):
        """
        Test Case: test_landing_contains_hello_world
        Verifies that the response body contains the string 'Hello, world!'.
        """
        response = self.client.get(reverse('core:landing'))
        self.assertContains(response, 'Hello, world!')

    def test_landing_uses_base_template(self):
        """
        Test Case: test_landing_uses_base_template
        Verifies that the view uses both 'landing.html' and the 'base.html' it extends.
        """
        response = self.client.get(reverse('core:landing'))
        self.assertTemplateUsed(response, 'landing.html')
        self.assertTemplateUsed(response, 'base.html')

    def test_landing_no_thai_characters(self):
        """
        Test Case: test_landing_no_thai_characters
        Verifies that the rendered HTML does not contain any characters from the
        Thai Unicode block (U+0E00 to U+0E7F).
        """
        response = self.client.get(reverse('core:landing'))
        html_content = response.content.decode('utf-8')
        # Regex for the Thai Unicode character range
        thai_char_pattern = r'[\u0E00-\u0E7F]'
        self.assertIsNone(re.search(thai_char_pattern, html_content))