# Production Deployment Guide for GhidulFit365

This guide provides instructions for deploying the GhidulFit365 fitness blog to a Hostinger VPS with PostgreSQL.

## Prerequisites

- A Hostinger VPS with Ubuntu/Debian
- Domain name (ghidulfit365.ro) pointed to your VPS IP (69.62.119.15)
- SSH access to your VPS

## Deployment Steps

### 1. Prepare the Local Project

1. Make sure your project is ready for production:
   - Debug mode is set to False in settings.py
   - Database is configured for PostgreSQL
   - Static and media files paths are configured correctly
   - Secret key is set to use environment variables

2. Commit all changes to your repository

### 2. Upload Project to VPS

1. Connect to your VPS via SSH:
   ```
   ssh root@69.62.119.15
   ```

2. Create a directory for your project:
   ```
   mkdir -p /var/www/ghidulfit365
   ```

3. Upload your project to the VPS using SCP or Git:
   ```
   # Using SCP (from your local machine)
   scp -r /path/to/your/local/project/* root@69.62.119.15:/var/www/ghidulfit365/

   # OR using Git (on the VPS)
   cd /var/www/ghidulfit365
   git clone <your-repository-url> .
   ```

### 3. Run the Deployment Script

1. Make the deployment script executable:
   ```
   chmod +x /var/www/ghidulfit365/deploy.sh
   ```

2. Run the deployment script:
   ```
   cd /var/www/ghidulfit365
   ./deploy.sh
   ```

   This script will:
   - Install system dependencies
   - Set up PostgreSQL database
   - Configure Python virtual environment
   - Install Python dependencies
   - Apply migrations
   - Collect static files
   - Configure Nginx
   - Set up Gunicorn service

### 4. Set Up SSL Certificate

After the deployment script completes, set up SSL with Let's Encrypt:

```
certbot --nginx -d ghidulfit365.ro -d www.ghidulfit365.ro
```

### 5. Update Nginx Configuration

After SSL is set up, uncomment the SSL sections in the Nginx configuration:

```
nano /etc/nginx/sites-available/ghidulfit365
```

Uncomment the SSL server blocks and the redirect in the HTTP server block.

### 6. Restart Nginx

```
systemctl restart nginx
```

## Maintenance

### Updating the Website

To update the website after making changes:

1. Upload the new files to the server
2. Apply migrations if needed:
   ```
   cd /var/www/ghidulfit365
   source venv/bin/activate
   python manage.py migrate
   ```
3. Collect static files if needed:
   ```
   python manage.py collectstatic --noinput
   ```
4. Restart Gunicorn:
   ```
   systemctl restart gunicorn
   ```

### Checking Logs

- Gunicorn logs:
  ```
  tail -f /var/log/gunicorn/error.log
  tail -f /var/log/gunicorn/access.log
  ```

- Nginx logs:
  ```
  tail -f /var/log/nginx/ghidulfit365.error.log
  tail -f /var/log/nginx/ghidulfit365.access.log
  ```

### Database Backup

To backup the PostgreSQL database:

```
pg_dump -U ghidulfit365_user -W -F c ghidulfit365 > /path/to/backup/ghidulfit365_$(date +%Y%m%d).dump
```

To restore from a backup:

```
pg_restore -U ghidulfit365_user -W -d ghidulfit365 /path/to/backup/ghidulfit365_YYYYMMDD.dump
```

## Google AdSense Integration

The website is already set up for Google AdSense with publisher ID: `pub-5227061222218296`.

### Verifying AdSense Setup

1. **Check ads.txt**
   - After deployment, verify that the ads.txt file is accessible at: `https://ghidulfit365.ro/ads.txt`
   - It should contain: `google.com, pub-5227061222218296, DIRECT, f08c47fec0942fa0`

2. **AdSense Locations**
   - The website has several predefined AdSense locations that can be managed in the Django admin panel
   - Log in to the admin panel and go to "Locații AdSense" to manage ad placements

3. **Troubleshooting AdSense**
   - If ads are not showing, check the browser console for errors
   - Verify that the AdSense account is approved and active
   - Make sure the ads.txt file is correctly set up and accessible

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check if Gunicorn is running: `systemctl status gunicorn`
   - Check Gunicorn logs for errors: `tail -f /var/log/gunicorn/error.log`

2. **Static Files Not Loading**
   - Verify paths in settings.py
   - Check permissions: `chmod -R 755 /var/www/ghidulfit365/staticfiles`
   - Ensure Nginx configuration is correct

3. **Database Connection Issues**
   - Check PostgreSQL is running: `systemctl status postgresql`
   - Verify database credentials in settings.py
   - Check PostgreSQL logs: `tail -f /var/log/postgresql/postgresql-*.log`

4. **AdSense Not Working**
   - Verify ads.txt is accessible: `curl https://ghidulfit365.ro/ads.txt`
   - Check if the AdSense script is loaded in the page source
   - Ensure there are no Content Security Policy issues

### Getting Help

If you encounter issues not covered in this guide, please contact your system administrator or refer to the Django documentation for more information.
