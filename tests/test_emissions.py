import unittest

from co2_tracker.emissions import Emissions
from co2_tracker.units import Energy
from co2_tracker.external.geography import CloudMetadata, GeoMetadata

from tests.testutils import get_test_data_source


class TestEmissions(unittest.TestCase):
    def setUp(self) -> None:
        # GIVEN
        self._data_source = get_test_data_source()
        self._emissions = Emissions(self._data_source)

    def test_get_emissions_CLOUD_AWS(self):
        # WHEN

        emissions = self._emissions.get_cloud_emissions(
            Energy.from_energy(kwh=0.6),
            CloudMetadata(provider="aws", region="us-east-1"),
        )

        # THEN
        assert isinstance(emissions, float)
        self.assertAlmostEqual(emissions, 0.22, places=2)

    def test_emissions_CLOUD_AZURE(self):
        # WHEN
        emissions = self._emissions.get_cloud_emissions(
            Energy.from_energy(kwh=1.5),
            CloudMetadata(provider="azure", region="eastus"),
        )

        # THEN
        assert isinstance(emissions, float)
        self.assertAlmostEqual(emissions, 0.55, places=2)

    def test_emissions_CLOUD_GCP(self):
        emissions = self._emissions.get_cloud_emissions(
            Energy.from_energy(kwh=0.01),
            CloudMetadata(provider="gcp", region="us-central1"),
        )

        # THEN
        assert isinstance(emissions, float)
        self.assertAlmostEqual(emissions, 0.01, places=2)

    def test_get_emissions_PRIVATE_INFRA_USA_WITH_REGION(self):
        # WHEN
        emissions = self._emissions.get_private_infra_emissions(
            Energy.from_energy(kwh=0.3),
            GeoMetadata(
                country_name="United States", country_iso_code="USA", region="Illinois"
            ),
        )

        # THEN
        assert isinstance(emissions, float)
        self.assertAlmostEqual(emissions, 0.11, places=2)

    def test_get_emissions_PRIVATE_INFRA_USA_WITHOUT_REGION(self):
        # WHEN
        emissions = self._emissions.get_private_infra_emissions(
            Energy.from_energy(kwh=0.3),
            GeoMetadata(country_name="United States", country_iso_code="USA"),
        )

        # THEN
        assert isinstance(emissions, float)
        self.assertAlmostEqual(emissions, 0.20, places=2)

    def test_get_emissions_PRIVATE_INFRA_USA_WITHOUT_COUNTRYNAME(self):
        # WHEN
        emissions = self._emissions.get_private_infra_emissions(
            Energy.from_energy(kwh=0.3), GeoMetadata(country_iso_code="USA")
        )

        # THEN
        assert isinstance(emissions, float)
        self.assertAlmostEqual(emissions, 0.20, places=2)

    def test_get_emissions_PRIVATE_INFRA_CANADA(self):

        # WHEN
        emissions = self._emissions.get_private_infra_emissions(
            Energy.from_energy(kwh=3),
            GeoMetadata(country_name="Canada", country_iso_code="CAN"),
        )

        # THEN
        assert isinstance(emissions, float)
        self.assertAlmostEqual(emissions, 1.6, places=2)
