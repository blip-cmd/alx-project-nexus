"""
Django management command to create sample data for the movie recommendation system.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from movies.models import Movie, Genre, Tag
from ratings.models import Rating, Favorite, WatchHistory


class Command(BaseCommand):
    help = 'Create sample data for the movie recommendation system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--movies',
            type=int,
            default=50,
            help='Number of movies to create'
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of test users to create'
        )
        parser.add_argument(
            '--ratings',
            type=int,
            default=200,
            help='Number of ratings to create'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🎬 Creating sample data for Movie Recommendation System...')
        )

        # Create genres
        genres_data = [
            {'name': 'Action', 'description': 'High-energy films with exciting sequences'},
            {'name': 'Comedy', 'description': 'Films designed to entertain and amuse'},
            {'name': 'Drama', 'description': 'Serious films with emotional themes'},
            {'name': 'Horror', 'description': 'Films designed to frighten and create suspense'},
            {'name': 'Romance', 'description': 'Films focused on love and relationships'},
            {'name': 'Sci-Fi', 'description': 'Science fiction films set in the future'},
            {'name': 'Thriller', 'description': 'Suspenseful films that keep viewers on edge'},
            {'name': 'Adventure', 'description': 'Films with exciting journeys and quests'},
            {'name': 'Animation', 'description': 'Animated films for all ages'},
            {'name': 'Documentary', 'description': 'Non-fiction films about real events'},
        ]

        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults={'description': genre_data['description']}
            )
            if created:
                self.stdout.write(f'✅ Created genre: {genre.name}')

        # Create tags
        tags_data = [
            'Blockbuster', 'Award Winner', 'Classic', 'Independent', 'Foreign',
            'Family Friendly', 'Dark', 'Uplifting', 'Thought Provoking', 'Funny',
            'Scary', 'Romantic', 'Action Packed', 'Emotional', 'Inspiring'
        ]

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'✅ Created tag: {tag.name}')

        # Sample movie data
        movies_data = [
            {
                'title': 'The Dark Knight',
                'description': 'Batman faces the Joker in this epic superhero film.',
                'release_date': '2008-07-18',
                'duration': 152,
                'imdb_rating': 9.0,
                'genres': ['Action', 'Drama', 'Thriller'],
                'tags': ['Blockbuster', 'Award Winner', 'Dark']
            },
            {
                'title': 'Inception',
                'description': 'A thief enters dreams to plant ideas in this mind-bending thriller.',
                'release_date': '2010-07-16',
                'duration': 148,
                'imdb_rating': 8.8,
                'genres': ['Sci-Fi', 'Action', 'Thriller'],
                'tags': ['Blockbuster', 'Thought Provoking']
            },
            {
                'title': 'The Shawshank Redemption',
                'description': 'A banker finds hope and friendship in prison.',
                'release_date': '1994-09-23',
                'duration': 142,
                'imdb_rating': 9.3,
                'genres': ['Drama'],
                'tags': ['Classic', 'Award Winner', 'Inspiring']
            },
            {
                'title': 'Pulp Fiction',
                'description': 'Interconnected stories of crime in Los Angeles.',
                'release_date': '1994-10-14',
                'duration': 154,
                'imdb_rating': 8.9,
                'genres': ['Drama', 'Thriller'],
                'tags': ['Classic', 'Award Winner', 'Independent']
            },
            {
                'title': 'The Godfather',
                'description': 'The aging patriarch transfers control of his empire to his son.',
                'release_date': '1972-03-24',
                'duration': 175,
                'imdb_rating': 9.2,
                'genres': ['Drama'],
                'tags': ['Classic', 'Award Winner']
            },
            {
                'title': 'Forrest Gump',
                'description': 'A simple man experiences historical events firsthand.',
                'release_date': '1994-07-06',
                'duration': 142,
                'imdb_rating': 8.8,
                'genres': ['Drama', 'Romance', 'Comedy'],
                'tags': ['Award Winner', 'Inspiring', 'Emotional']
            },
            {
                'title': 'The Matrix',
                'description': 'A hacker discovers reality is a computer simulation.',
                'release_date': '1999-03-31',
                'duration': 136,
                'imdb_rating': 8.7,
                'genres': ['Sci-Fi', 'Action'],
                'tags': ['Blockbuster', 'Thought Provoking']
            },
            {
                'title': 'Titanic',
                'description': 'A romance unfolds aboard the doomed ship.',
                'release_date': '1997-12-19',
                'duration': 194,
                'imdb_rating': 7.8,
                'genres': ['Romance', 'Drama'],
                'tags': ['Blockbuster', 'Award Winner', 'Romantic']
            },
            {
                'title': 'The Lion King',
                'description': 'A young lion prince flees his kingdom after his father\'s death.',
                'release_date': '1994-06-24',
                'duration': 88,
                'imdb_rating': 8.5,
                'genres': ['Animation', 'Adventure'],
                'tags': ['Family Friendly', 'Classic', 'Inspiring']
            },
            {
                'title': 'Avatar',
                'description': 'A marine on an alien planet becomes torn between two worlds.',
                'release_date': '2009-12-18',
                'duration': 162,
                'imdb_rating': 7.8,
                'genres': ['Sci-Fi', 'Action', 'Adventure'],
                'tags': ['Blockbuster', 'Action Packed']
            },
            {
                'title': 'Goodfellas',
                'description': 'The story of a mob associate and his rise through the ranks.',
                'release_date': '1990-09-21',
                'duration': 146,
                'imdb_rating': 8.7,
                'genres': ['Drama'],
                'tags': ['Classic', 'Award Winner']
            },
            {
                'title': 'Casablanca',
                'description': 'A nightclub owner helps his former lover and her husband escape.',
                'release_date': '1942-11-26',
                'duration': 102,
                'imdb_rating': 8.5,
                'genres': ['Drama', 'Romance'],
                'tags': ['Classic', 'Romantic']
            },
            {
                'title': 'The Avengers',
                'description': 'Earth\'s mightiest heroes unite to save the world.',
                'release_date': '2012-05-04',
                'duration': 143,
                'imdb_rating': 8.0,
                'genres': ['Action', 'Adventure', 'Sci-Fi'],
                'tags': ['Blockbuster', 'Action Packed']
            },
            {
                'title': 'Spirited Away',
                'description': 'A girl enters a world of spirits to save her parents.',
                'release_date': '2001-07-20',
                'duration': 125,
                'imdb_rating': 9.3,
                'genres': ['Animation', 'Adventure'],
                'tags': ['Award Winner', 'Family Friendly', 'Foreign']
            },
            {
                'title': 'Parasite',
                'description': 'A poor family schemes to infiltrate a wealthy household.',
                'release_date': '2019-05-30',
                'duration': 132,
                'imdb_rating': 8.6,
                'genres': ['Drama', 'Thriller'],
                'tags': ['Award Winner', 'Foreign', 'Thought Provoking']
            }
        ]

        # Create movies from sample data
        created_movies = []
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data['description'],
                    'release_date': movie_data['release_date'],
                    'duration': movie_data['duration'],
                    'imdb_rating': movie_data['imdb_rating'],
                    'popularity_score': random.randint(60, 100)
                }
            )
            
            if created:
                # Add genres
                for genre_name in movie_data['genres']:
                    genre = Genre.objects.get(name=genre_name)
                    movie.genres.add(genre)
                
                # Add tags
                for tag_name in movie_data['tags']:
                    tag = Tag.objects.get(name=tag_name)
                    movie.tags.add(tag)
                
                created_movies.append(movie)
                self.stdout.write(f'✅ Created movie: {movie.title}')

        # Create additional random movies if needed
        additional_movies_needed = options['movies'] - len(created_movies)
        if additional_movies_needed > 0:
            self.stdout.write(f'Creating {additional_movies_needed} additional random movies...')
            
            for i in range(additional_movies_needed):
                movie_number = len(created_movies) + i + 1
                movie = Movie.objects.create(
                    title=f'Movie {movie_number}',
                    description=f'This is a sample movie #{movie_number} for testing purposes.',
                    release_date=timezone.now().date() - timedelta(days=random.randint(1, 3650)),
                    duration=random.randint(80, 180),
                    imdb_rating=round(random.uniform(5.0, 9.5), 1),
                    popularity_score=random.randint(40, 100)
                )
                
                # Add random genres
                genres = Genre.objects.all()
                movie.genres.add(*random.sample(list(genres), random.randint(1, 3)))
                
                # Add random tags
                tags = Tag.objects.all()
                movie.tags.add(*random.sample(list(tags), random.randint(1, 4)))
                
                created_movies.append(movie)

        self.stdout.write(f'✅ Total movies created: {len(created_movies)}')

        # Create test users
        test_users = []
        for i in range(options['users']):
            username = f'testuser{i+1}'
            email = f'testuser{i+1}@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'Test{i+1}',
                    'last_name': 'User'
                }
            )
            
            if created:
                user.set_password('testpassword123')
                user.save()
                test_users.append(user)
                self.stdout.write(f'✅ Created user: {user.username}')

        self.stdout.write(f'✅ Total users: {User.objects.count()}')

        # Create ratings
        all_movies = Movie.objects.all()
        all_users = User.objects.all()
        
        ratings_created = 0
        for _ in range(options['ratings']):
            user = random.choice(all_users)
            movie = random.choice(all_movies)
            
            # Don't create duplicate ratings
            if not Rating.objects.filter(user=user, movie=movie).exists():
                rating = Rating.objects.create(
                    user=user,
                    movie=movie,
                    rating=random.randint(1, 5),
                    review=f'Sample review by {user.username} for {movie.title}' if random.choice([True, False]) else None,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 365))
                )
                ratings_created += 1

        self.stdout.write(f'✅ Created ratings: {ratings_created}')

        # Create some favorites
        favorites_created = 0
        for _ in range(options['ratings'] // 4):  # About 25% of ratings become favorites
            user = random.choice(all_users)
            movie = random.choice(all_movies)
            
            if not Favorite.objects.filter(user=user, movie=movie).exists():
                Favorite.objects.create(
                    user=user,
                    movie=movie,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 365))
                )
                favorites_created += 1

        self.stdout.write(f'✅ Created favorites: {favorites_created}')

        # Create some watch history
        watch_history_created = 0
        for _ in range(options['ratings'] // 2):  # About 50% of ratings have watch history
            user = random.choice(all_users)
            movie = random.choice(all_movies)
            
            if not WatchHistory.objects.filter(user=user, movie=movie).exists():
                WatchHistory.objects.create(
                    user=user,
                    movie=movie,
                    progress_minutes=random.randint(10, movie.duration),
                    watched_at=timezone.now() - timedelta(days=random.randint(1, 365))
                )
                watch_history_created += 1

        self.stdout.write(f'✅ Created watch history entries: {watch_history_created}')

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('🎉 Sample data creation complete!'))
        self.stdout.write(f'📊 Summary:')
        self.stdout.write(f'   • Movies: {Movie.objects.count()}')
        self.stdout.write(f'   • Genres: {Genre.objects.count()}')
        self.stdout.write(f'   • Tags: {Tag.objects.count()}')
        self.stdout.write(f'   • Users: {User.objects.count()}')
        self.stdout.write(f'   • Ratings: {Rating.objects.count()}')
        self.stdout.write(f'   • Favorites: {Favorite.objects.count()}')
        self.stdout.write(f'   • Watch History: {WatchHistory.objects.count()}')
        self.stdout.write('\n🚀 You can now test the API with real data!')
        self.stdout.write('💡 Use the testing guide (TESTING_GUIDE.md) to explore the API endpoints.')
