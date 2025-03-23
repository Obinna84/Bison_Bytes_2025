import requests
import base64
import os
from typing import Tuple, List, Optional

class SpotifyAPI:
    # Replace with your actual credentials (use environment variables for security)
    CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '3efaa366d55c47c68906dc1d5338ef2c')
    CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '36a67ec8de6d49bc8c7c38a449211966')

    @staticmethod
    def get_spotify_token() -> str:
        """Get Spotify access token"""
        auth_url = "https://accounts.spotify.com/api/token"
        auth_header = base64.b64encode(f"{SpotifyAPI.CLIENT_ID}:{SpotifyAPI.CLIENT_SECRET}".encode("utf-8")).decode("utf-8")
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        response = requests.post(auth_url, headers=headers, data=data)
        response_data = response.json()
        return response_data['access_token']

    @staticmethod
    def get_artist_profile(artist_name: str) -> Tuple[Optional[str], Optional[str], Optional[List[str]]]:
        """Get artist profile and top tracks from Spotify"""
        token = SpotifyAPI.get_spotify_token()
        search_url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(search_url, headers=headers)
        artist_data = response.json()
        
        if artist_data['artists']['items']:
            artist_info = artist_data['artists']['items'][0]
            artist_name = artist_info['name']
            artist_id = artist_info['id']
            
            # Get top tracks of the artist
            top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
            top_tracks_response = requests.get(top_tracks_url, headers=headers)
            top_tracks_data = top_tracks_response.json()
            
            top_tracks = [track['name'] for track in top_tracks_data['tracks']]
            
            artist_image_url = artist_info['images'][0]['url'] if artist_info['images'] else None
            
            return artist_name, artist_image_url, top_tracks
        else:
            return None, None, None

    @staticmethod
    def get_genai_recommendations(user_input: str) -> Tuple[Optional[str], Optional[str], Optional[List[str]], List[List[str]]]:
        """Get recommendations from GenAI"""
        api_key = os.getenv('GENAI_API_KEY', 'AIzaSyCfHkhojPHEByUSRV7DXPZpQwUC5_E5KYo')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        data = {
            "contents": [{
                "parts": [{"text": f"""
                    Without added explanation or an introduction, determine whether the following input is an artist name, genre, or vibe: {user_input}.
                    Please respond with just "artist," "genre," or "vibe."
                """}]
            }]
        }

        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        
        if response.status_code == 200:
            generated_content = response.json()
            classification = generated_content['candidates'][0]['content']['parts'][0]['text'].strip()
            
            if classification == "artist":
                # Fetch artist recommendations from GenAI
                artist_name, artist_image_url, top_tracks = SpotifyAPI.get_artist_profile(user_input)
                recommendations = SpotifyAPI.get_recommendations(user_input)
                return artist_name, artist_image_url, top_tracks, recommendations
            else:
                # Fetch genre/vibe recommendations from GenAI
                recommendations = SpotifyAPI.get_recommendations(user_input)
                return None, None, None, recommendations
        else:
            print(f"Error: {response.status_code}")
            return None, None, None, []

    @staticmethod
    def get_recommendations(user_input: str) -> List[List[str]]:
        """Get recommendations from GenAI"""
        api_key = os.getenv('GENAI_API_KEY', 'AIzaSyCfHkhojPHEByUSRV7DXPZpQwUC5_E5KYo')
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        data = {
            "contents": [{
                "parts": [{"text": f"""
                    Without added explanation or an introduction, recommend (5 each in most to least recommended order) genres, artists, songs, and albums based on the following: {user_input}.
                    Please provide the response in this format:
                    - Artists: [artist1, artist2, artist3]
                    - Genres: [genre1, genre2, genre3]
                    - Albums: [album1, album2, album3]
                    - Songs: [song1, song2, song3]
                """}]
            }]
        }

        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        
        if response.status_code == 200:
            generated_content = response.json()
            recommended_content = generated_content['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # Parse and return results
            artists, genres, albums, songs = [], [], [], []
            for line in recommended_content.split('\n'):
                line = line.strip()
                if line.startswith('- Artists:'):
                    artists = line.replace('- Artists:', '').strip().strip('[]').split(',')
                elif line.startswith('- Genres:'):
                    genres = line.replace('- Genres:', '').strip().strip('[]').split(',')
                elif line.startswith('- Albums:'):
                    albums = line.replace('- Albums:', '').strip().strip('[]').split(',')
                elif line.startswith('- Songs:'):
                    songs = line.replace('- Songs:', '').strip().strip('[]').split(',')
            
            return [artists, genres, albums, songs]
        else:
            print(f"Error: {response.status_code}")
            return [[], [], [], []]

    def return_useful_info(self, user_input: str) -> dict:
        """Return useful information based on user input"""
        artist_name, artist_image_url, top_tracks, recommendations = self.get_genai_recommendations(user_input)
        info = {
            "artist_name": artist_name,
            "artist_image_url" : artist_image_url,
            "top_tracks": top_tracks,
            "recommended_artists": recommendations[0],
            "recommended_artists_images": [SpotifyAPI.get_artist_profile(i)[1] for i in recommendations[0]],
            "recommended_genres": recommendations[1],
            "recommended_albums": recommendations[2]
        }
        return info


# Example usage
if __name__ == "__main__":
    api_instance = SpotifyAPI()
    user_input = "Drake"
    info = api_instance.return_useful_info(user_input)
    print("Recommended Artists:", info["artists"])
    print("Recommended Genres:", info["genres"])
    print("Recommended Albums:", info["albums"])
    print("Recommended Songs:", info["songs"])