from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play, Performance, TheatreHall, Genre, Actor
from theatre.serializers import PlayDetailSerializer, PlayListSerializer


PLAY_URL = reverse("theatre:play-list")


def sample_play(**params):
    defaults = {
        "title": "test_title",
        "description": "test_description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "test_genre",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "test_first", "last_name": "test_last"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        name="test_performance",
        rows=1,
        seats_in_row=1
    )

    defaults = {
        "show_time": "2024-01-24 00:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="test_password"
        )

        self.client.force_authenticate(self.user)

    def test_list_of_plays(self):
        sample_play()
        play_with_genre = sample_play(title="test_genre")
        play_with_actor = sample_play(title="test_actor")

        genre = sample_genre(name="test")
        actor = sample_actor(first_name="test_name")

        play_with_genre.genre.add(genre)
        play_with_actor.actor.add(actor)

        response = self.client.get(PLAY_URL)

        plays_from_response = response.data.get("results", [])

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(plays_from_response, serializer.data)

    def test_filter_plays_by_title(self):
        test_play1 = sample_play(title="Play")
        test_play2 = sample_play(title="test")

        response = self.client.get(PLAY_URL, {"title": "te"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue("results" in response.data)
        titles = [play["title"] for play in response.data["results"]]
        self.assertNotIn(test_play1.title, titles)
        self.assertIn(test_play2.title, titles)

    def test_filter_plays_by_genre(self):
        test_genre = sample_genre(name="test_genre")
        test_play1 = sample_play(title="test_genre1")
        test_play2 = sample_play(title="test_genre2")
        test_play1.genre.add(test_genre)
        test_play2.genre.add(test_genre)

        response = self.client.get(PLAY_URL, {"genre": test_genre.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        titles = [play["title"] for play in response.data["results"]]
        self.assertIn(test_play1.title, titles)
        self.assertIn(test_play2.title, titles)

    def test_play_detail(self):
        temp_play = sample_play()
        url = detail_url(temp_play.id)
        response = self.client.get(url)
        serializer = PlayDetailSerializer(temp_play)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_play_detail(self):
        play = sample_play(title="Test")
        genre = sample_genre(name="Test")

        play.genre.add(genre)

        url = detail_url(play.id)

        response = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "Test Title",
            "description": "Test Description",
        }
        response = self.client.post(PLAY_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    class AdminPlayApiTest(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = get_user_model().objects.create_user(
                "testadmin@test.com", "test_password", is_staff=True
            )
            self.client.force_authenticate(self.user)

        def test_create_play(self):
            payload = {
                "title": "Test Title",
                "description": "Test Description",
            }

            response = self.client.post(PLAY_URL, payload)
            play = Play.objects.get(id=response.data["id"])

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            for key in payload:
                self.assertEqual(payload[key], getattr(play, key))
