import random

from django.core.management import BaseCommand
from django.db.models import Avg
from django.utils import timezone

from films.models import Producer, Film, Genre, Actor
from interactions.models import Interaction
from users.models import User


class Command(BaseCommand):
    help = 'Заполнение базы данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--num_films',
            type=int,
            default=100,
            help='Количество фильмов для генерации (по умолчанию: 100)',
        )
        parser.add_argument(
            '--num_users',
            type=int,
            default=50,
            help='Количество пользователей для генерации (по умолчанию: 50)',
        )
        parser.add_argument(
            '--num_producers',
            type=int,
            default=20,
            help='Количество режиссеров для генерации (по умолчанию: 30)',
        )
        parser.add_argument(
            '--num_actors',
            type=int,
            default=20,
            help='Количество актеров для генерации (по умолчанию: 50)',
        )

    def handle(self, *args, **options):
        num_films = options['num_films']
        num_users = options['num_users']
        num_producers = options['num_producers']
        num_actors = options['num_actors']

        print('Очищаю базу данных...')

        Genre.objects.all().delete()
        Producer.objects.all().delete()
        Actor.objects.all().delete()
        Film.objects.all().delete()
        User.objects.all().delete()
        Interaction.objects.all().delete()

        print('Создаю жанры...')

        genres = [
            'Drama', 'Detective', 'Romance', 'Comedy',
            'History', 'Science fiction', 'Thriller', 'Biography',
            'Documentary', 'Action', 'Horror',
        ]

        genre_objects = [Genre(name=name) for name in genres]
        Genre.objects.bulk_create(genre_objects)
        genres = Genre.objects.all()

        print(f'Создаю режиссеров...')
        producer_list = [Producer(name=f'Режиссер {i}', bio=f'Режиссер {i} Биография') for i in range(1, num_producers + 1)]
        Producer.objects.bulk_create(producer_list)
        producers = Producer.objects.all()

        print(f'Создаю актеров...')
        actor_list = [Producer(name=f'Актер {i}', bio=f'Актер {i} Биография') for i in range(1, num_actors + 1)]
        Actor.objects.bulk_create(actor_list)
        actors = Actor.objects.all()

        print(f'Создаю фильмы...')
        films = []
        for i in range(1, num_films + 1):

            film = Film(
                title=f'Фильм {i}',
                producer=random.choice(producers),
                description=f'Описание фильма {i}',
                publish_date=timezone.now().date(),
                release_year=random.randint(1930, 2025),
            )
            films.append(film)

        Film.objects.bulk_create(films)

        print('Присваиваю фильмам жанры и добавляю актеров...')
        all_films = Film.objects.all()
        for film in all_films:
            film.genres.add(*random.sample(list(genres), k=random.randint(1, 3)))
            film.actors.add(*random.sample(list(actors), k=random.randint(2, 5)))

        print('Создаю пользователей...')
        for i in range(1, num_users + 1):
            user = User.objects.create_user(
                email=f'test_user_{i}@example.com',
                password='password'
            )
            user.preferred_genres.add(*random.sample(list(genres), k=random.randint(2, 4)))

        self.stdout.write('Создаю взаимосвязи...')
        interactions = []
        all_films = list(Film.objects.all())
        all_users = User.objects.all()

        for user in all_users:
            user_preferred_genres = user.preferred_genres.all()
            preferred_films = Film.objects.filter(genres__in=user_preferred_genres).distinct()
            other_films = Film.objects.exclude(genres__in=user_preferred_genres).distinct()

            num_interactions = random.randint(10, 21)
            num_preferred = int(num_interactions * 0.7)
            num_other = num_interactions - num_preferred

            try:
                preferred_sample = random.sample(list(preferred_films), num_preferred)
                other_sample = random.sample(list(other_films), num_other)
            except ValueError:
                continue

            for film in preferred_sample + other_sample:
                rating = random.choices(
                    [None, round(random.uniform(3.0, 5.0), 1)],
                    weights=[0.3, 0.7]
                )[0]

                interactions.append(Interaction(
                    user=user,
                    film=film,
                    rating=rating,
                ))

        Interaction.objects.bulk_create(interactions)

        self.stdout.write('Пересчитываю средний рейтинг фильмов...')
        films_to_update = Film.objects.filter(interaction__isnull=False).distinct()
        for film in films_to_update:
            film.average_rating = Interaction.objects.filter(film=film).aggregate(
                Avg('rating')
            )['rating__avg'] or 0.0
            film.save()

        print(
            f'Успешно создано:\n'
            f'- {Genre.objects.count()} жанров\n'
            f'- {Producer.objects.count()} режиссеров\n'
            f'- {Film.objects.count()} фильмов\n'
            f'- {Actor.objects.count()} актеров\n'
            f'- {User.objects.count()} пользователей\n'
            f'- {Interaction.objects.count()} взаимодействий'
        )
