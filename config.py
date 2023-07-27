# Secrets
update_key = "changeme"
secret = "s-s4t2ud-"
key = "u-s4t2ud-"
telegram_token = ''

# Configuration
redirect_url = "https://{current_domain}/auth"
auth_link = f"https://api.intra.42.fr/oauth/authorize?client_id={key}&redirect_uri={redirect_url}&response_type=code&scope=public"
redis_host = "127.0.0.1"
redis_port = 6379
campuses_to_update = [1, 53]
