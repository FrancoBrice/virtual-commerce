npm run build
sudo rm -rf /var/www/frontend

sudo mkdir -p /var/www/frontend
sudo cp -r build/* /var/www/frontend/

sudo systemctl restart nginx