# Get monthly listeners for a list of local bands

The script takes a pre-defined list of bands from a Python list (`local_bands.py`) and fetches monthly listener and social links for each band having a Spotify profile.

## Things to know:
- The script doesn't use an official Spotify API so the token is a short-lived session token you need to grab from an active web session (use dev tools to grab the Authorization Bearer token from an xhr `query` request.)
- Bands without a spotify profile are fine to include in the `local_bands.py` file they just won't have stats included in the output.
- Genres and notes are set in the `local_bands.py` file, not from Spotify (Spotify has genres but not at the band level.)
- Social links specified in the `local_bands.py` file will be used in place of Spotify provided links if set. This is to support adding social links to a band who doesn't have them set up in Spotify (I'm looking at you Sara Adams.)


## Setup & run
1. Create your virtual env or whatever `python -m venv ./.venv`
2. `pip install -r requirements.txt`
3. Set token: `export SPOTIFY_ACCESS_TOKEN="Bearer <token>"` where token is grabbed from a Spotify web request using dev tools (e.g. [https://open.spotify.com/artist/5anRy2kwFKkwtewYlCX0RZ](https://open.spotify.com/artist/5anRy2kwFKkwtewYlCX0RZ))
4. Update `local_bands.py` with any new bands, notes, or whatever you want to be included in the output.
5. Run it: `python app.py`

A csv file with a timestamp will be written to the root directory. Enjoy.

❗ Don't forget to commit and push any changs made to the `local_bands.py` file.
