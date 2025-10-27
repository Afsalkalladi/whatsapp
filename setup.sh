#!/bin/bash

# Quick Setup Script for WhatsApp CV Manager
# This script helps you set up the project quickly

echo "🚀 WhatsApp CV Manager - Quick Setup"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your credentials."
else
    echo ""
    echo "✅ .env file already exists."
fi

# Run migrations
echo ""
echo "Running Django migrations..."
python manage.py migrate

# Create superuser prompt
echo ""
echo "Do you want to create a Django superuser? (y/n)"
read -r create_superuser

if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

echo ""
echo "============================================"
echo "✅ Setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Add your Google credentials.json file"
echo "3. Run: python manage.py runserver"
echo "4. Set up ngrok: ngrok http 8000"
echo "5. Configure WhatsApp webhook with ngrok URL"
echo ""
echo "Happy coding! 🎉"
