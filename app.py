from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Function to fetch YouTube videos based on query using YouTube Data API
def fetch_youtube_videos(query):
    api_key = "AIzaSyBOc-m5ZTxlswmUisY_Avt-OQVxyncQecQ"  # Your provided YouTube API key
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            videos = []
            for item in data['items'][:3]:  # Get top 3 videos
                videos.append({
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'thumbnail': item['snippet']['thumbnails']['high']['url']  # Adding thumbnail image
                })
            return videos
        else:
            return []
    except Exception as e:
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form['query']  # Get query from the form data

    # Fetch relevant YouTube videos based on the query
    videos = fetch_youtube_videos(query)

    # Return the response with videos
    return jsonify({'videos': videos})

@app.route('/ask', methods=['GET'])
def ask_page():
    return render_template('ask.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        # Here, you can add logic to save the file or process it
        return jsonify({"message": "File uploaded successfully!"})
    return jsonify({"error": "No file uploaded!"})

if __name__ == '__main__':
    app.run(debug=True)
