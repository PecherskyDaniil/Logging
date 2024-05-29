cd serveridusers
uvicorn main:app --host=10.128.0.27 --port=8000 &
sleep 2s
cd ..
python3 ./publisher/publisher.py &
sleep 2s
python3 ./subscriber/subscriber.py &