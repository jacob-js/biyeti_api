from decouple import config as env

environment = env('environment')

db_name = env('DB_NAME')
db_user = env('DB_USER')
db_password = env('DB_PASSWORD')
db_host = env('DB_HOST')
db_port = env('DB_PORT')

private_key= env('PRIVATE_KEY')
g_client_id = env('GOOGLE_CLIENT_ID')
g_client_secret = env('GOOGLE_CLIENT_SECRET')
cloudinary_name = env('CLOUDINARY_NAME')
cloudinary_api_key = env('CLOUDINARY_API_KEY')
cloudinary_api_secret = env('CLOUDINARY_API_SECRET')

email_host = env('EMAIL_HOST')
email_port = env('EMAIL_PORT')
email_host_user = env('EMAIL_HOST_USER')
email_host_password = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
