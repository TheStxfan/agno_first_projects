@echo off

@REM https://www.composerize.com/

@REM wsl --shutdown

cd agentos-docker

@REM docker compose down --remove-orphans
@REM docker compose up -d --force-recreate --build
@REM docker compose down
@REM docker compose build --no-cache
@REM docker compose up -d

docker compose down
docker compose up

pause