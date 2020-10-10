import git
import os
import subprocess as cmd


print("Cloning Git Repo")
if not os.path.exists("/project"):
    os.makedirs("/project")
git.Git("/project").clone("https://github.com/a2z-ice/eureka-server")
#os.system("chmod -R 775 /project/eureka-server/")
os.chdir("/project/eureka-server/")

print("Building Project")
os.system("mvn package -Dspring.profiles.active=docker")

print("Building Docker")
os.system("docker build -f Dockerfile -t eureka-server .")

print("Login to docker registry")
os.system("docker login --username=ronisudip --password=Ghosh@#123")

print("Pushing docker image to docker hub")
os.system("docker tag eureka-server ronisudip/eureka-server:v1")
os.system("docker push ronisudip/eureka-server:v1")

print("Deleteing docker image from local repository")
os.system("docker rmi eureka-server")
os.system("docker rmi ronisudip/eureka-server:v1")

print("Pull docker image from dockerhub")
os.system("docker pull ronisudip/eureka-server:v1")

print("Run docker image in container")
os.system("docker run --network devops-net --name eureka-server -p 8761:8761 -d ronisudip/eureka-server:v1")

print("Saving docker container log")
os.system("docker inspect --format='{{.LogPath}}' eureka-server > /project/docker.log")

