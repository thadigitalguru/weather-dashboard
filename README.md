# Weather & Traffic Dashboard for Nairobi

An interactive weather and traffic monitoring dashboard for Nairobi and surrounding areas, featuring real-time weather updates, traffic conditions, and community-driven updates through Twitter integration.

> 🌐 **[Live Dashboard Preview](http://127.0.0.1:5000)** - Access the live dashboard locally after installation

## Features

### 🌤️ Weather Information
- Real-time weather data from OpenWeatherMap API
- Temperature, humidity, wind speed, and more
- Visual weather indicators and icons
- Feels-like temperature and visibility information

### 🚗 Traffic Monitoring
- Live traffic status for major roads
- Traffic conditions simulation based on time of day
- Visual indicators (green/yellow/red) for traffic levels
- Interactive road status cards

### 🎮 Gamification
- Traffic Navigation Score (0-100)
- Score changes based on current traffic conditions
- Achievement messages based on your score
- Interactive elements and animations

### 🐦 Twitter Integration
- Real-time community updates
- Location-specific hashtags
- Post traffic and weather updates
- View recent tweets about traffic conditions

### 📍 Supported Locations
- Nairobi CBD
- Kikuyu
- Thika
- Machakos
- Kiambu
- Ongata Rongai

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```env
OPENWEATHER_API_KEY=your_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_SECRET=your_twitter_access_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
```

5. Run the application:
```bash
python app.py
```

6. Open http://127.0.0.1:5000 in your browser

## API Keys Setup

### OpenWeatherMap API
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your API key from the dashboard
3. Add it to your `.env` file

### Twitter API
1. Apply for a [Twitter Developer Account](https://developer.twitter.com/en/apply-for-access)
2. Create a new project and app
3. Get your API keys and tokens
4. Add them to your `.env` file

## Tech Stack

- **Frontend**:
  - HTML5, CSS3, JavaScript
  - Bootstrap 5.3
  - Chart.js for data visualization
  - Font Awesome icons
  - Custom CSS animations

- **Backend**:
  - Python 3.11
  - Flask web framework
  - Flask-SQLAlchemy
  - Python-dotenv for environment variables

- **APIs & Services**:
  - OpenWeatherMap API
  - Twitter API v2
  - Custom traffic simulation service

- **Development Tools**:
  - Git for version control
  - Visual Studio Code
  - Python virtual environment

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenWeatherMap for weather data
- Twitter for community updates integration
- Bootstrap team for the UI framework
- All contributors and users of this dashboard
