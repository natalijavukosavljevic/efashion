from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
    #kada se signal trigeruje
    def ready(self):
        import store.signals
