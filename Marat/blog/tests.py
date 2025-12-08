from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Club, Post, Comment
from unittest.mock import patch
from blog.forms import CommentForm
from django.urls import reverse, resolve
from blog import views
from django.test import SimpleTestCase
from django.test import TestCase, Client


class EmailTest(TestCase):

    def setUp(self):
        self.club = Club.objects.create(
            name="Juventus",
            country="Italy",
            founded=1897,
            stadium="Allianz"
        )

        self.post = Post.objects.create(
            title="Juve",
            content="Forza Juve",
            club=self.club,
            author="Admin"
        )

        self.user = User.objects.create_user(username="tester", password="12345")

    @patch("blog.views.send_mail")
    def test_email_sent(self, mock_send):
        self.client.login(username="tester", password="12345")

        response = self.client.post(
            reverse("post_detail", args=[self.post.id]),
            {"subject": "Email Test", "text": "Text"}
        )

        self.assertEqual(response.status_code, 302)
        mock_send.assert_called_once()


class CommentFormTest(TestCase):

    def test_valid_form(self):
        form = CommentForm(data={
            "subject": "Hello",
            "text": "World"
        })
        self.assertTrue(form.is_valid())

    def test_missing_subject(self):
        form = CommentForm(data={
            "subject": "",
            "text": "Test"
        })
        self.assertFalse(form.is_valid())

    def test_missing_text(self):
        form = CommentForm(data={
            "subject": "Title",
            "text": ""
        })
        self.assertFalse(form.is_valid())


class ModelsTest(TestCase):

    def setUp(self):
        self.club = Club.objects.create(
            name="Real Madrid",
            country="Spain",
            founded=1902,
            stadium="Santiago Bernabéu"
        )

        self.post = Post.objects.create(
            title="Test Post",
            content="Test content",
            club=self.club,
            author="Admin"
        )

        self.user = User.objects.create_user(username="testuser", password="12345")

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            subject="Subject",
            text="Text",
            is_published=True
        )

    def test_club_str(self):
        self.assertEqual(str(self.club), "Real Madrid")

    def test_post_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_comment_str(self):
        self.assertEqual(str(self.comment), "Subject — testuser")



class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, views.HomeClubListView)

    def test_post_list(self):
        url = reverse('post_list')
        self.assertEqual(resolve(url).func.view_class, views.PostListView)

    def test_search_url(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func.view_class, views.SearchView)

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)



class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.club = Club.objects.create(
            name="Barcelona",
            country="Spain",
            founded=1899,
            stadium="Camp Nou"
        )

        self.post = Post.objects.create(
            title="Visca Barca",
            content="Barca content",
            club=self.club,
            author="Admin"
        )

        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "club_list.html")

    def test_post_list_view(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("posts", response.context)

    def test_club_detail_view(self):
        response = self.client.get(reverse("club_detail", args=[self.club.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_requires_login(self):
        response = self.client.get(reverse("post_detail", args=[self.post.id]))
        self.assertRedirects(response, f"/ru/login/?next=/ru/post/{self.post.id}/")

    def test_post_comment_submit(self):
        self.client.login(username="testuser", password="12345")

        with patch("blog.signals.send_mail") as mock_mail:
            response = self.client.post(
                reverse("post_detail", args=[self.post.id]),
                {"subject": "Test subject", "text": "Test text"}
            )

            self.assertEqual(response.status_code, 302)
            self.assertEqual(Comment.objects.count(), 1)
            self.assertTrue(mock_mail.called)  


    def test_register_view(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
