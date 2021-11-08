import environ
environ.Env.read_env()
env = environ.Env()

db_host = env('DB_HOST')
db_user = env('DB_USER')
db_pass = env('DB_PASS')
db_name = env('DB_NAME')
db_host = env('DB_HOST')
db_port = env('DB_PORT')

private_key= env('PRIVATE_KEY')