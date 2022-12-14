"""
Tests for models.
"""

from django.test import TestCase
from core import models
from django.contrib.auth import get_user_model
from decimal import Decimal
from unittest.mock import patch


def create_user(
    email="user@example.com",
    password="testpass123",
):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successfull"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""

        sample_emails = [
            ["test@EXAMPLE.com", "test@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password="sample123"
            )
            self.assertEqual(user.email, expected)

    def test_create_recibe(self):
        """Test creating a recipe is successfull"""
        user = get_user_model().objects.create_user(
            "test@example.com",
            "testpass123",
        )

        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description",
        )

        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successfull"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name="Tag1")

        self.assertEquals(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successfull"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user, name="Ingredient1"
        )

        self.assertEquals(str(ingredient), ingredient.name)

    @patch("core.models.uuid.uuid4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test generating image path"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/recipe/{uuid}.jpg")
