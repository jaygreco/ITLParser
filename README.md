# ITLParser
Apple ITL .plist pre-parser for Apple Music --> Spotify transition.
Slices an iTunes library by date. I use the day I became an Apple Music subscriber, since I have all of the earlier songs on disk.
Removes (feat) in the song title and removes multiple artists in the artist field, since this messes with the Spotify import.

After preprocessing, I followed [this](https://medium.com/@adrian_cooney/how-to-move-from-apple-music-to-spotify-6d4192c634b0) to import the playlist into spotify. Here's the line you care about: `polytunes import --from apple --to spotify --apple-library Library_parsed.xml playlist_name`

Use at your own risk.
