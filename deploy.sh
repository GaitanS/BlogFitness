#!/bin/bash

# Exit on error
set -e

# Variables
PROJECT_NAME="ghidulfit365"
PROJECT_PATH="/var/www/$PROJECT_NAME"
VENV_PATH="$PROJECT_PATH/venv"
NGINX_CONF="/etc/nginx/sites-available/$PROJECT_NAME"
NGINX_ENABLED="/etc/nginx/sites-enabled/$PROJECT_NAME"
SYSTEMD_SERVICE="/etc/systemd/system/gunicorn.service"
LOG_DIR="/var/log/gunicorn"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting deployment of $PROJECT_NAME...${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root${NC}"
  exit 1
fi

# Create project directory
echo -e "${YELLOW}Creating project directory...${NC}"
mkdir -p $PROJECT_PATH
mkdir -p $PROJECT_PATH/media
mkdir -p $LOG_DIR

# Install system dependencies
echo -e "${YELLOW}Installing system dependencies...${NC}"
apt-get update
apt-get install -y python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx

# Create PostgreSQL database and user
echo -e "${YELLOW}Setting up PostgreSQL...${NC}"
sudo -u postgres psql -c "CREATE DATABASE $PROJECT_NAME;"
sudo -u postgres psql -c "CREATE USER ${PROJECT_NAME}_user WITH PASSWORD 'adrianvilea2025';"
sudo -u postgres psql -c "ALTER ROLE ${PROJECT_NAME}_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE ${PROJECT_NAME}_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE ${PROJECT_NAME}_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $PROJECT_NAME TO ${PROJECT_NAME}_user;"

# Copy project files
echo -e "${YELLOW}Copying project files...${NC}"
cp -r . $PROJECT_PATH/

# Set permissions
echo -e "${YELLOW}Setting permissions...${NC}"
chown -R www-data:www-data $PROJECT_PATH
chmod -R 755 $PROJECT_PATH

# Create and activate virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
python3 -m venv $VENV_PATH
source $VENV_PATH/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r $PROJECT_PATH/requirements.txt
pip install gunicorn psycopg2-binary

# Apply migrations and collect static files
echo -e "${YELLOW}Applying migrations...${NC}"
cd $PROJECT_PATH
python manage.py migrate
python manage.py collectstatic --noinput

# Ensure ads.txt is properly set up
echo -e "${YELLOW}Setting up ads.txt...${NC}"
cp $PROJECT_PATH/templates/ads.txt $PROJECT_PATH/staticfiles/
chown www-data:www-data $PROJECT_PATH/staticfiles/ads.txt
chmod 644 $PROJECT_PATH/staticfiles/ads.txt

# Configure Nginx
echo -e "${YELLOW}Configuring Nginx...${NC}"
cp $PROJECT_PATH/nginx-ghidulfit365 $NGINX_CONF
ln -sf $NGINX_CONF $NGINX_ENABLED

# Configure Gunicorn systemd service
echo -e "${YELLOW}Configuring Gunicorn service...${NC}"
cp $PROJECT_PATH/gunicorn.service $SYSTEMD_SERVICE
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn

# Restart Nginx
echo -e "${YELLOW}Restarting Nginx...${NC}"
systemctl restart nginx

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Set up SSL with: certbot --nginx -d ghidulfit365.ro -d www.ghidulfit365.ro"
echo -e "2. Uncomment SSL sections in Nginx config after SSL is set up"
echo -e "3. Restart Nginx after SSL setup: systemctl restart nginx"
