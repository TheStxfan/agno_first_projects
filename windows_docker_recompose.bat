@echo off

@REM https://www.composerize.com/

@REM wsl --shutdown

cd agentos-docker

@REM docker compose down --remove-orphans
@REM docker compose up -d --force-recreate --build
docker compose down
@REM docker compose build --no-cache
docker compose up

@REM docker build --no-cache --progress=plain -t barista-twin .
@REM docker run --gpus all -it barista-twin

@REM docker compose down
@REM docker compose up

@REM docker container prune

pause