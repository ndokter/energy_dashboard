from apps.logger.models import AbstractReading
from apps.logger.models.abstract_reading import ReadingReportsQuerySet


class GasReading(AbstractReading):
    objects = ReadingReportsQuerySet.as_manager()
