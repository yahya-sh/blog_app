from abc import ABC, abstractmethod


class BaseSeeder(ABC):
    """
    Base class for all seeders.
    """

    app_label = None
    depends_on = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if cls.app_label is None:
            cls.app_label = cls._infer_app_label()

    @classmethod
    def _infer_app_label(cls):
        return cls.__module__.split(".")[0]

    @abstractmethod
    def run(self, **options):
        pass