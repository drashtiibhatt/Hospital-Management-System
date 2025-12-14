from app import create_app

# Vercel needs a top-level variable named `app` or `handler`
app = create_app("production")
