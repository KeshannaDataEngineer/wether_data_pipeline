#!/bin/bash


PROJECT_ID="your-project-id" 
IMAGE_NAME="weather-data-pipeline"
IMAGE_TAG="latest"  
REGION="us-central1"  


echo "Building Docker image..."
docker build -t gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG .


echo "Authenticating with Google Cloud..."
gcloud auth login


echo "Setting Google Cloud project..."
gcloud config set project $PROJECT_ID


echo "Pushing Docker image to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG


echo "Deploying to Google Cloud Run..."
gcloud run deploy $IMAGE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME:$IMAGE_TAG \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated  

echo "Deployment completed successfully!"
