from django.contrib.auth.base_user import BaseUserManager


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, last_name, username, password, **extra_fields):
        if first_name is None:
            raise ValueError('Users should have First Name')
        if last_name is None:
            raise ValueError('Users should have Last Name')
        if username is None:
            raise ValueError('Users should have Username')
        if email is None:
            raise ValueError('Users should have an Email Address')
        if password is None:
            raise ValueError('Password cannot be empty')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, first_name, last_name, username, password, **extra_fields)

    def create_superuser(self, email, first_name, last_name, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff must have is_staff=True.')
        return self._create_user(email, first_name, last_name, username, password, **extra_fields)
