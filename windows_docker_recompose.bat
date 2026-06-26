@echo off

wsl --shutdown

cd agentos-docker

docker compose down --remove-orphans
@REM docker compose up -d --force-recreate --build
docker compose build --no-cache
docker compose up -d
pause