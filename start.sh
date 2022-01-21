alembic upgrade head
MODE=$1
if [ "$MODE" = "--reload" ]
then
    echo "Running in development mode (with reload)"
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Running in production mode (no reload)"
    uvicorn app.main:app --host 0.0.0.0 --port 8000
fi