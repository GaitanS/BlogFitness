# Gunicorn configuration file
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"

# Process naming
proc_name = "ghidulfit365"

# Worker timeout
timeout = 30

# Keep the workers alive
keepalive = 2