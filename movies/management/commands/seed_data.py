"""
Django management command to seed the database with sample data.
This populates movies, genres, and sample users for testing.
"""
import random
from decimal import Decimal
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from movies.models import Movie, Genre, Tag
from ratings.models import Rating, Favorite

class Command(BaseCommand):
    help = 'Seed the database with sample movies, genres, and test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of test users to create (default: 5)',
        )
        parser.add_argument(
            '--movies',
            type=int,
            default=50,
            help='Number of movies to create (default: 50)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🎬 Starting database seeding...')
        )

        try:
            with transaction.atomic():
                # Create genres
                self.create_genres()
                
                # Create tags
                self.create_tags()
                
                # Create movies
                movies_count = options['movies']
                self.create_movies(movies_count)
                
                # Create test users
                users_count = options['users']
                self.create_users(users_count)
                
                # Create sample ratings
                self.create_sample_ratings()

            self.stdout.write(
                self.style.SUCCESS('✅ Database seeding completed successfully!')
            )
            
            # Display summary
            self.display_summary()

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Seeding failed: {str(e)}')
            )

    def create_genres(self):
        """Create movie genres."""
        genres_data = [
            ('Action', 'High-energy films with exciting sequences, stunts, and adventure'),
            ('Comedy', 'Films intended to make audiences laugh through humor'),
            ('Drama', 'Serious films that portray realistic characters and situations'),
            ('Horror', 'Films intended to frighten, unsettle, and create suspense'),
            ('Romance', 'Films focused on love stories and romantic relationships'),
            ('Sci-Fi', 'Films featuring futuristic concepts and advanced technology'),
            ('Thriller', 'Films that keep audiences on edge with suspense and excitement'),
            ('Fantasy', 'Films featuring magical or supernatural elements'),
            ('Crime', 'Films centered around criminal activities and law enforcement'),
            ('Documentary', 'Non-fiction films that document reality'),
            ('Animation', 'Films created using animated techniques'),
            ('Family', 'Films suitable for all ages and family viewing'),
            ('Adventure', 'Films featuring exciting journeys and exploration'),
            ('Mystery', 'Films involving puzzles, secrets, and investigations'),
            ('War', 'Films depicting military conflicts and wartime experiences'),
        ]

        for name, description in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            if created:
                self.stdout.write(f'  ➕ Created genre: {name}')

    def create_tags(self):
        """Create movie tags."""
        tags_data = [
            'blockbuster', 'indie', 'oscar-winner', 'cult-classic', 'remake',
            'sequel', 'trilogy', 'based-on-book', 'based-on-true-story', 'superhero',
            'zombie', 'vampire', 'time-travel', 'space', 'dystopian', 'coming-of-age',
            'heist', 'martial-arts', 'musical', 'western', 'film-noir', 'psychological',
            'black-and-white', 'foreign', 'silent', 'epic', 'biographical', 'period-piece'
        ]

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'  ➕ Created tag: {tag_name}')

    def create_movies(self, count):
        """Create sample movies."""
        # Sample movie data
        movie_titles = [
            "The Last Adventure", "Midnight in Paris", "Digital Revolution", "Ocean's Mystery",
            "The Time Keeper", "Neon Dreams", "Dark Horizon", "City of Angels", "The Explorer",
            "Quantum Leap", "The Storyteller", "Crimson Sky", "The Guardian", "Silent Valley",
            "The Architect", "Blue Moon", "The Warrior", "Electric Storm", "The Journey Home",
            "Shadow of Tomorrow", "The Alchemist", "Crystal Lake", "The Phoenix", "Golden Hour",
            "The Navigator", "Starlight Express", "The Collector", "Thunder Road", "The Dreamer",
            "Silver Lining", "The Professor", "Wild River", "The Artist", "Broken Chains",
            "The Messenger", "Copper Mountain", "The Scientist", "Frozen Time", "The Inventor",
            "Violet Storm", "The Chronicler", "Desert Winds", "The Magician", "Autumn Leaves",
            "The Philosopher", "Winter's Tale", "The Conductor", "Spring Awakening", "The Writer",
            "Summer Nights", "The Teacher", "Endless Sky", "The Healer"
        ]

        descriptions = [
            "An epic journey through uncharted territories filled with danger and wonder.",
            "A heartwarming story about friendship, love, and second chances.",
            "A thrilling adventure that challenges the boundaries of reality.",
            "A mysterious tale that keeps you guessing until the very end.",
            "An inspiring story about overcoming impossible odds.",
            "A visually stunning masterpiece that redefines cinema.",
            "A gripping drama that explores the depths of human nature.",
            "An action-packed thriller with unexpected twists and turns.",
            "A beautiful romance set against breathtaking landscapes.",
            "A thought-provoking film that questions everything we believe."
        ]

        genres = list(Genre.objects.all())
        tags = list(Tag.objects.all())
        
        if not genres:
            self.stdout.write(self.style.WARNING('No genres found. Creating basic genres first.'))
            self.create_genres()
            genres = list(Genre.objects.all())

        movies_created = 0
        for i in range(count):
            if i < len(movie_titles):
                title = movie_titles[i]
            else:
                title = f"Sample Movie {i + 1}"

            # Check if movie already exists
            if Movie.objects.filter(title=title).exists():
                continue

            movie = Movie.objects.create(
                title=title,
                description=random.choice(descriptions),
                release_date=self.random_date(),
                duration=random.randint(90, 180),
                poster_image=f"https://picsum.photos/300/450?random={i}",
                trailer_url=f"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                imdb_rating=round(random.uniform(5.0, 9.0), 1),
                popularity_score=random.randint(1, 100),
            )

            # Add random genres (1-3 genres per movie)
            movie_genres = random.sample(genres, random.randint(1, min(3, len(genres))))
            movie.genres.set(movie_genres)

            # Add random tags (0-4 tags per movie)
            if tags:
                movie_tags = random.sample(tags, random.randint(0, min(4, len(tags))))
                movie.tags.set(movie_tags)

            movies_created += 1
            if movies_created % 10 == 0:
                self.stdout.write(f'  ➕ Created {movies_created} movies...')

        self.stdout.write(f'  ✅ Created {movies_created} movies total')

    def create_users(self, count):
        """Create test users."""
        usernames = [
            'moviefan1', 'cinephile2', 'filmcritic3', 'viewer4', 'watcher5',
            'reviewer6', 'moviebuff7', 'cinema8', 'screen9', 'reel10'
        ]

        users_created = 0
        for i in range(count):
            if i < len(usernames):
                username = usernames[i]
            else:
                username = f'testuser{i + 1}'

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                continue

            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='testpass123',
                first_name=f'Test{i + 1}',
                last_name='User'
            )
            users_created += 1

        self.stdout.write(f'  ✅ Created {users_created} test users')

    def create_sample_ratings(self):
        """Create sample ratings between users and movies."""
        users = list(User.objects.filter(is_superuser=False))
        movies = list(Movie.objects.all())

        if not users or not movies:
            self.stdout.write(self.style.WARNING('No users or movies found. Skipping ratings.'))
            return

        ratings_created = 0
        favorites_created = 0

        for user in users:
            # Each user rates 20-40% of movies randomly
            num_ratings = random.randint(
                int(len(movies) * 0.2), 
                int(len(movies) * 0.4)
            )
            
            rated_movies = random.sample(movies, num_ratings)
            
            for movie in rated_movies:
                # Create rating
                Rating.objects.get_or_create(
                    user=user,
                    movie=movie,
                    defaults={
                        'score': Decimal(str(round(random.uniform(1.0, 5.0), 1))),
                        'review': f"Great movie! Really enjoyed watching {movie.title}." if random.random() > 0.7 else ""
                    }
                )
                ratings_created += 1

                # 30% chance to add to favorites (only highly rated movies)
                if random.random() < 0.3:
                    Favorite.objects.get_or_create(
                        user=user,
                        movie=movie
                    )
                    favorites_created += 1

        self.stdout.write(f'  ✅ Created {ratings_created} ratings')
        self.stdout.write(f'  ✅ Created {favorites_created} favorites')

    def random_date(self):
        """Generate random release date between 1990 and 2024."""
        start_date = date(1990, 1, 1)
        end_date = date(2024, 12, 31)
        
        time_between = end_date - start_date
        days_between = time_between.days
        
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)

    def display_summary(self):
        """Display seeding summary."""
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS("📊 SEEDING SUMMARY"))
        self.stdout.write("="*50)
        
        self.stdout.write(f"🎭 Genres: {Genre.objects.count()}")
        self.stdout.write(f"🏷️  Tags: {Tag.objects.count()}")
        self.stdout.write(f"🎬 Movies: {Movie.objects.count()}")
        self.stdout.write(f"👥 Users: {User.objects.count()} (including admin)")
        self.stdout.write(f"⭐ Ratings: {Rating.objects.count()}")
        self.stdout.write(f"❤️  Favorites: {Favorite.objects.count()}")
        
        self.stdout.write("\n🎯 Next Steps:")
        self.stdout.write("1. Visit your admin panel to see the data")
        self.stdout.write("2. Test API endpoints with the new data")
        self.stdout.write("3. Try user login with: username=moviefan1, password=testpass123")
        self.stdout.write("\n✅ Database is now ready for testing!")