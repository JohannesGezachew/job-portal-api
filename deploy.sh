#!/bin/bash

# This script helps with manually triggering a new deployment on Render
# You can run this after making changes to your codebase

echo "Preparing to deploy to Render..."

# Step 1: Add your changes to git
git add .

# Step 2: Commit your changes
echo "Enter a commit message:"
read commit_message
git commit -m "$commit_message"

# Step 3: Push to GitHub (this will trigger a new deployment on Render)
echo "Pushing changes to GitHub..."
git push origin main

echo "Done! Changes have been pushed to GitHub."
echo "Render should automatically start building a new deployment."
echo "Check your Render dashboard for deployment status."
echo "Remember that the first request after redeployment may take 50+ seconds to process." 