set -a
[ -f ../.env ] && . ../.env
set +a

uvicorn main:app --host 0.0.0.0 --port 5010 --reload