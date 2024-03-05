import os

GoogleAPIKey = os.environ.get("GOOGLE_API_KEY")

if GoogleAPIKey is None:
    print("Environment variable 'GOOGLE_API_KEY' not found.")
else:
    print("Found environment variable 'GOOGLE_API_KEY':", GoogleAPIKey)
