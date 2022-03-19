import os
import environ
environ.Env.read_env()
env = environ.Env()

private_key= env('PRIVATE_KEY')
g_client_id = env('GOOGLE_CLIENT_ID')
g_client_secret = env('GOOGLE_CLIENT_SECRET')
cloudinary_name = env('CLOUDINARY_NAME')
cloudinary_api_key = env('CLOUDINARY_API_KEY')
cloudinary_api_secret = env('CLOUDINARY_API_SECRET')