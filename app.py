from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import random
import tweepy

app = Flask(__name__)

load_dotenv()

# Load environment variables
API_KEY = os.getenv('OPENWEATHER_API_KEY')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Twitter client setup
try:
    client = tweepy.Client(
        bearer_token=TWITTER_BEARER_TOKEN,
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET
    )
except Exception as e:
    print(f"Twitter client setup failed: {e}")
    client = None

# Predefined locations in and around Nairobi with major roads
KENYA_LOCATIONS = {
    'nairobi': {
        'name': 'Nairobi CBD',
        'lat': -1.2921,
        'lon': 36.8219,
        'roads': [
            {'name': 'Mombasa Road', 'traffic_prone': True},
            {'name': 'Thika Road', 'traffic_prone': True},
            {'name': 'Waiyaki Way', 'traffic_prone': True}
        ],
        'hashtags': ['#NairobiTraffic', '#MombasaRoad', '#ThikaRoad']
    },
    'kikuyu': {
        'name': 'Kikuyu',
        'lat': -1.2451,
        'lon': 36.6619,
        'roads': [
            {'name': 'Waiyaki Way', 'traffic_prone': True},
            {'name': 'Kikuyu Road', 'traffic_prone': False}
        ],
        'hashtags': ['#KikuyuTraffic', '#WaiyakiWay']
    },
    'thika': {
        'name': 'Thika',
        'lat': -1.0396,
        'lon': 37.0900,
        'roads': [
            {'name': 'Thika Superhighway', 'traffic_prone': True},
            {'name': 'Garissa Road', 'traffic_prone': False}
        ],
        'hashtags': ['#ThikaTraffic', '#ThikaRoad']
    },
    'machakos': {
        'name': 'Machakos',
        'lat': -1.5177,
        'lon': 37.2634,
        'roads': [
            {'name': 'Mombasa Road', 'traffic_prone': True},
            {'name': 'Machakos Road', 'traffic_prone': False}
        ],
        'hashtags': ['#MachakosTraffic', '#MombasaRoad']
    },
    'kiambu': {
        'name': 'Kiambu',
        'lat': -1.1712,
        'lon': 36.8357,
        'roads': [
            {'name': 'Kiambu Road', 'traffic_prone': True},
            {'name': 'Northern Bypass', 'traffic_prone': False}
        ],
        'hashtags': ['#KiambuTraffic', '#KiambuRoad']
    },
    'ongata_rongai': {
        'name': 'Ongata Rongai',
        'lat': -1.3963,
        'lon': 36.7457,
        'roads': [
            {'name': 'Magadi Road', 'traffic_prone': True},
            {'name': 'Langata Road', 'traffic_prone': True}
        ],
        'hashtags': ['#RongaiTraffic', '#MagadiRoad']
    }
}

def get_traffic_status(road, hour):
    """Simulate traffic status based on time and road characteristics"""
    rush_hours = [7, 8, 9, 17, 18, 19]
    if road['traffic_prone'] and hour in rush_hours:
        return random.choice(['heavy', 'moderate', 'heavy'])
    elif road['traffic_prone']:
        return random.choice(['light', 'moderate', 'light'])
    return random.choice(['light', 'light', 'moderate'])

def calculate_traffic_score(traffic_statuses):
    """Calculate traffic navigation score based on traffic conditions"""
    score_map = {'light': 30, 'moderate': 20, 'heavy': 10}
    return sum(score_map[status] for status in traffic_statuses)

def get_recent_tweets(hashtags, max_results=5):
    """Get recent tweets for the given hashtags"""
    try:
        tweets = []
        query = ' OR '.join(hashtags)
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=['created_at', 'author_id']
        )
        if response.data:
            tweets = [
                {
                    'text': tweet.text,
                    'created_at': tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
                for tweet in response.data
            ]
        return tweets
    except Exception as e:
        print(f"Error fetching tweets: {str(e)}")
        return []

@app.route('/')
def home():
    return render_template('index.html', locations=KENYA_LOCATIONS)

@app.route('/post_update', methods=['POST'])
def post_update():
    try:
        data = request.json
        location = data.get('location')
        message = data.get('message')
        
        if not location or not message or location not in KENYA_LOCATIONS:
            return jsonify({'error': 'Invalid request'}), 400

        # Add relevant hashtags to the message
        hashtags = ' '.join(KENYA_LOCATIONS[location]['hashtags'])
        full_message = f"{message} {hashtags}"
        
        # Post to Twitter
        tweet = client.create_tweet(text=full_message)
        
        return jsonify({'success': True, 'tweet_id': tweet.data['id']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/weather')
def get_weather():
    location = request.args.get('location', 'nairobi').lower()
    
    if location not in KENYA_LOCATIONS:
        return jsonify({'error': 'Location not supported'}), 400

    location_data = KENYA_LOCATIONS[location]
    current_hour = datetime.now().hour
    
    # Get traffic status for each road
    roads_with_traffic = []
    traffic_statuses = []
    for road in location_data['roads']:
        traffic_status = get_traffic_status(road, current_hour)
        traffic_statuses.append(traffic_status)
        roads_with_traffic.append({
            'name': road['name'],
            'status': traffic_status
        })

    # Calculate traffic score
    traffic_score = calculate_traffic_score(traffic_statuses)

    # Get recent tweets for this location
    recent_tweets = get_recent_tweets(location_data['hashtags'])

    params = {
        'lat': location_data['lat'],
        'lon': location_data['lon'],
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_data = {
                'city': location_data['name'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'].capitalize(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),
                'feels_like': round(data['main']['feels_like']),
                'pressure': data['main']['pressure'],
                'visibility': data.get('visibility', 0) / 1000,
                'sunrise': data['sys']['sunrise'],
                'sunset': data['sys']['sunset'],
                'roads': roads_with_traffic,
                'traffic_score': traffic_score,
                'tweets': recent_tweets,
                'hashtags': location_data['hashtags']
            }
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'Weather data not available'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
