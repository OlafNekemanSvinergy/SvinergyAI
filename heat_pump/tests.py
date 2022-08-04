from django.test import TestCase
from .models import HeatPump, HeatPumpBrand


# Create your tests here.
class HeatPumpModelTests(TestCase):

    def test_successfully_committed_heat_pump(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        heat_pump = HeatPump(brand=HeatPumpBrand.BOSCH, max_power=2000)

        self.assertIs(heat_pump.brand, HeatPumpBrand.BOSCH)
