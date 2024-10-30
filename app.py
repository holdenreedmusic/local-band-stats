import time
import requests
import csv
import os
import datetime
from typing import List
from dataclasses import dataclass
import local_bands

@dataclass
class Band:
    name: str
    spotify_id: str
    genres: List[str]
    notes: str
    monthly_listeners: int = 0
    social_links: str = ''

def main():

  # This would apply if we used the official Spotify API but it doesn't provide listeners stats
  # creds = get_spotify_api_creds()

  # use short lived user session token grabbed from spotify web client (filter xhrs on 'operation') and set with:
  # export SPOTIFY_ACCESS_TOKEN="Bearer <token>"
  access_token = os.environ.get('SPOTIFY_ACCESS_TOKEN')
  path_prefix = '&variables=%7B%22uri%22%3A%22spotify%3Aartist%3A'
  path_suffix = '%22%2C%22locale%22%3A%22%22%2C%22includePrerelease%22%3Atrue%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2216e6bf9b0ab93a784463928e82acd4fe5546cd582cb5cf14290cbb171b4fcf72%22%7D%7D'
  api_url = 'https://api-partner.spotify.com/pathfinder/v1/query?operationName=queryArtistOverview'

  # Optional headers (if needed for authentication, etc.)
  headers = {
      'Authorization': f'{access_token}',
      'Content-Type': 'application/json'
  }

  bands = [] #List[Band]
  # new up band classes with defaults values
  for b in local_bands.list():
    # initialize band with static & default data
    band = Band(
      name=b['name'],
      spotify_id=b.get('spotify_id', False) or '',
      genres=b.get('genres', False) or [],
      notes=b.get('notes', False) or '',
      social_links=b.get('social_links', False) or ''
    )
    # print(band)
    bands.append(band)

  # loop the band list and merge spotify data with static data
  for band in bands:
    try:
        if band.spotify_id == '':
          continue

        url = f'{api_url}{path_prefix}{band.spotify_id}{path_suffix}'
        # Make the GET request to the API
        response = requests.get(url, headers=headers)

        if response.status_code == 401:
          print('You need to provide a fresh SPOTIFY_ACCESS_TOKEN env var')
          exit()

        # Api call is happy
        if response.status_code == 200:
            jdata = response.json()
            data = jdata['data']
            # print(data)

            # artist_name = data['artistUnion']['profile']['name']
            band.monthly_listeners = data['artistUnion']['stats']['monthlyListeners'] or 0
            links = []
            
            # if the social links are not set in the denver_bands.py file get them from spotify
            if band.social_links == '':
              for link in data['artistUnion']['profile']['externalLinks']['items']:
                links.append(link['url'])
              band.social_links = ' '.join(links)

        else:
            # boo
            print(f"Failed to get data for {id}: Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred for {id}: {e}")
    
    # Optional: wait a bit before making the next request (to avoid rate-limiting issues)
    # print(artists_info[idx])
    time.sleep(.1)

  write_csv(bands)


def create_filename(base_name):
  timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  filename = f"{base_name}_{timestamp}.csv"
  return filename

def write_csv(bands):
  print(len(bands))
  sorted_bands = sorted(bands, key=lambda x: x.monthly_listeners, reverse=True)
              
  with open(create_filename('denver_bands'), "w", newline="") as file:
    # Create a CSV writer object
    writer = csv.writer(file)

    # Write the header row
    writer.writerow(["Artist", "Monthly Listeners", "Spotify Link", "Social Links", "Genres", "Notes"])
    
    for band in sorted_bands:
      # if 'monthly_listeners' in artist_info:
      #   monthly_listeners = artist_info['monthly_listeners']
      # else:
      #   monthly_listeners = ''
      
      # if band:
      #   genres = artist_info['genres']
      # else:
      #   genres = ''
      
      # if 'external_links' in artist_info:
      #   links = artist_info['external_links']
      # else:
      #   links = ''
      
      if band.spotify_id != '':
        spotify_link = f'https://open.spotify.com/artist/{band.spotify_id}'
      else:
        spotify_link = ''

      row = [
        band.name,
        band.monthly_listeners,
        spotify_link,
        band.social_links,
        ','.join(band.genres),
        band.notes,
      ]
      writer.writerow(row)
  

# def get_spotify_api_creds():
  # Spotify API credentials (from Spotify Developer Dashboard)
  # client_id = '25db06a88755437188103fe964f7a169'
  # client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

  # Spotify API token URL
  # token_url = 'https://accounts.spotify.com/api/token'

  # Encode client credentials in base64
  # client_creds = f"{client_id}:{client_secret}"
  # client_creds_b64 = base64.b64encode(client_creds.encode()).decode()

  # Set the headers and body for the token request
  # headers = {
  #     'Authorization': f'Basic {client_creds_b64}',
  #     'Content-Type': 'application/x-www-form-urlencoded'
  # }
  # data = {
  #     'grant_type': 'client_credentials'
  # }

  # Make the request to get the access token
  # response = requests.post(token_url, headers=headers, data=data)
  # token_info = response.json()
  # print(token_info)
  # # Extract the access token
  # access_token = token_info['access_token']
  # return {"headers": headers, "data": data}

if __name__ == '__main__':
    main()