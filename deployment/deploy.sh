cd /home/naresh/Projects/Topaz
echo "Fecthing changes"
git pull

# Build image
echo "Building image"
docker build -t topaz:latest .

# Stop current container
echo "Stopping current deployment"
docker stop $(docker ps -q --filter ancestor=topaz:latest)

# Deploy
echo "Deploying"
docker run -d -v /home/naresh/Projects/Topaz/data/:/app/data/ -p 4000:5000 topaz:latest

# Clean up
echo "Cleaning up images"
docker images | grep none | awk '{print "docker rmi --force " $3;}' | sh

echo "Deploment complete!"
