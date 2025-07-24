from django.apps import AppConfig


class ResumesiteConfig(AppConfig):
    name = 'resumesite'

    def ready(self):
        import resumesite.signals
