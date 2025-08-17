#!/bin/bash

# Paraphrasing API - Quick Setup Script
# This script helps you deploy your monetizable paraphrasing API

echo "🚀 Paraphrasing API - Quick Setup"
echo "================================="
echo ""

# Check if git is available
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11+ first."
    exit 1
fi

echo "📦 Setting up your paraphrasing API..."

# Install dependencies
echo "Installing Python dependencies..."
if command -v pip &> /dev/null; then
    pip install -r requirements.txt
elif command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    echo "❌ pip is not available. Please install pip first."
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next Steps:"
echo "1. Test locally: python main.py"
echo "2. Visit: http://localhost:5000"
echo "3. Push to GitHub and deploy to Northflank"
echo "4. List on RapidAPI for monetization"
echo ""
echo "📚 Read DEPLOYMENT_GUIDE.md for complete instructions"
echo ""
echo "💰 Your API is ready to generate revenue!"