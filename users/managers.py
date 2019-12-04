from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, login_id, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not login_id:
            raise ValueError('The given login ID must be set')
        if not email:
            raise ValueError('The given email must be set')
        # username = self.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(login_id=login_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, login_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(login_id, email, password, **extra_fields)

    def create_superuser(self, login_id, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        account = self._create_user(login_id, email, password, **extra_fields)
        account.is_admin = True
        account.is_staff = True
        account.save()

        return account