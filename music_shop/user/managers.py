from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    @staticmethod
    def __validation(username, password=None):
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have a password")

    def create_user(self, username, password=None):
        self.__validation(username, password)

        user = self.model(username=username)
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False

        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        self.__validation(username, password)

        user = self.model(username=username)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True

        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password=None):
        self.__validation(username, password)
        user = self.model(username=username)

        user.set_password(password)
        user.is_admin = False
        user.is_staff = True

        user.save(using=self._db)
        return user
