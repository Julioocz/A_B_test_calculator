from django.test import TestCase

from . import ab_calculator


# Create your tests here.
class CalculatorTests(TestCase):
    def test_significance(self):
        """
        Tests the A/B split test significance for 2 cases:
            case1:
                - Visit numbers for the control version = 1000. Conversions = 100
                - Visit numbers for the variant version = 1000. Conversions = 150

                Expected result: 0.0383

            case 2:
                - Visit numbers for the control version = 500. Conversions = 30
                - Visit numbers for the variant version = 500. Conversions = 38

                Expected result: 0.1573
            """

        significance_case1 = ab_calculator.significance(size_a=1000, successes_a=100,
                                                        size_b=1000, successes_b=125)

        significance_case2 = ab_calculator.significance(size_a=500, successes_a=30,
                                                        size_b=500, successes_b=38)
        self.assertTrue(significance_case1 - 0.0383 <= 0.001)
        self.assertTrue(significance_case2 - 0.1573 <= 0.001)

    def test_get_method_index(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'calculator/index.html')

    def test_post_method_index(self):
        """The index view should do the a/b split test calculations on a post request."""
        response_json = self.client.post('/', {
            'visitors[control]': '600',
            'visitors[variant]': '700',
            'conversions[control]': '100',
            'conversions[variant]': '150',
        })
        resp = response_json.json()

        self.assertTrue(resp['significant'])
        self.assertTrue(resp['significance'] - 0.01419 < 0.0001)

    def test_response_status_code_is_400_when_missing_parameters(self):
        response_json = self.client.post('/', {
            'visitors[control]': '600',
            'conversions[control]': '100',
            'conversions[variant]': '150',
        })

        self.assertEqual(response_json.status_code, 400)

    def test_response_status_code_is_400_when_visitors_number_islower_than_conversions(self):
        response_json = self.client.post('/', {
            'visitors[control]': '90',
            'visitors[variant]': '700',
            'conversions[control]': '100',
            'conversions[variant]': '150',
        })

        self.assertEqual(response_json.status_code, 400)