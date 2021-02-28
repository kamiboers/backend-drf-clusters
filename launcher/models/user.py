from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def uri(self):
        return f'http://127.0.0.1:8000/users/{self.id}/'
