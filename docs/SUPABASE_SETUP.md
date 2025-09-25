# 🗄️ Supabase PostgreSQL Setup Guide

## 📋 Setup Instructions

### 1. Get Your Supabase Password
1. Go to your [Supabase Dashboard](https://app.supabase.com)
2. Select your project: `rgqovkaosbjeruqgzhee`
3. Navigate to **Settings** → **Database**
4. Copy your database password

### 2. Update Environment Variables
1. Open the `.env` file in your project root
2. Replace `[YOUR-PASSWORD]` with your actual Supabase password:
   ```
   DATABASE_URL=postgresql://postgres.rgqovkaosbjeruqgzhee:YOUR_ACTUAL_PASSWORD@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
   ```

### 3. Test Database Connection
Run the test script to verify your connection:
```bash
python test_db_connection.py
```

## 🔗 Supabase Connection Details

- **Host**: `aws-0-eu-central-1.pooler.supabase.com`
- **Port**: `6543`
- **Database**: `postgres`
- **Username**: `postgres.rgqovkaosbjeruqgzhee`
- **SSL**: Required (automatically handled)

## 🚀 Django Configuration

Once your connection is verified, Django will use these settings:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.rgqovkaosbjeruqgzhee',
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': 'aws-0-eu-central-1.pooler.supabase.com',
        'PORT': '6543',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}
```

## 🔐 Security Notes

- ✅ `.env` file is in `.gitignore` - your credentials are safe
- ✅ Use environment variables for all sensitive data
- ✅ Never commit passwords to version control
- ✅ Supabase uses SSL by default

## 📊 Database Features Available

With Supabase, you get:
- ✅ PostgreSQL 15+ with full SQL support
- ✅ Built-in connection pooling
- ✅ Automatic backups
- ✅ Real-time subscriptions (for future features)
- ✅ Row Level Security (RLS)
- ✅ RESTful API auto-generation

## 🛠️ Next Steps

1. Verify database connection
2. Initialize Django project
3. Create Django apps
4. Design database models
5. Run migrations

Your Supabase database is production-ready and will scale with your application! 🎉
