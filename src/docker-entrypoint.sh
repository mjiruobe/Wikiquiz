echo 'Starting db processing script'
cd app
python process.py &

echo 'Starting server'
uvicorn api:app --host 0.0.0.0