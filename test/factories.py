from factory import Faker, Factory

from main.models import User

from django.core.files.uploadedfile import SimpleUploadedFile
from faker.providers import BaseProvider


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
        )


Faker.add_provider(ImageFileProvider)


class UserFactory(Factory):
    username = Faker("user_name")
    password = Faker("password")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Faker("email")
    role = Faker("random_element", elements=User.Roles.values)
    avatar_picture = Faker("image_file", fmt="jpeg")

    class Meta:
        model = dict


class AdminFactory(UserFactory):
    is_superuser = True
    is_staff = True
