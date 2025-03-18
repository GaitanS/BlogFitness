# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "unix:/run/gunicorn.sock"
workers = multiprocessing.cpu_count() * 2 + 1

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "ghidulfit365"

# SSL
keyfile = "/etc/letsencrypt/live/ghidulfit365.ro/privkey.pem"
certfile = "/etc/letsencrypt/live/ghidulfit365.ro/fullchain.pem"

# Worker timeout
timeout = 30

# Keep the workers alive
keepalive = 2