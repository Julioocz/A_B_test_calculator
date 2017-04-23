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
        print(significance_case1, significance_case2)
        self.assertTrue(significance_case1 - 0.0383 <= 0.001, True)
        self.assertTrue(significance_case2 - 0.1573 <= 0.001, True)
