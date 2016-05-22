from django.apps import AppConfig
from django.db.models.signals import post_save


class EnergyDashboardBackEndAppConfig(AppConfig):
    name = 'energy_dashboard.back_end'
    verbose_name = "Energy Dashboard Back-end"

    def ready(self):
        from energy_dashboard.back_end.models import Reading
        from energy_dashboard.back_end.services import reading_post_save_handler

        post_save.connect(reading_post_save_handler, sender=Reading)
