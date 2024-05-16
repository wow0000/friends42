# Secrets
update_key = "changeme"
secret = "s-s4t2ud-"
key = "u-s4t2ud-"
bocal_token = "changeme"
telegram_token = ''
sentry = ''

# Configuration
redirect_url = "http://{current_domain}/auth"
auth_link = "https://api.intra.42.fr/oauth/authorize?client_id={key}&redirect_uri={redirect_url}&response_type=code&scope=public"
redis_host = "127.0.0.1"
redis_port = 6379
campuses_to_update = [1, 53, 66, 62, 31]
sentry_traces_sample_rate = 0.4
sentry_profiles_sample_rate = 0.4
