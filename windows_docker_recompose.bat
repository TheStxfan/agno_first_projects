@echo off

cd agentos-docker

docker compose down --remove-orphans
docker compose up -d --force-recreate --build

pause