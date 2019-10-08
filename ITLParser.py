import plistlib as pl
from datetime import datetime

date_string = "2016-07-03T00:00:00Z"

format_string = "%Y-%m-%dT%H:%M:%SZ"
cutoff = datetime.strptime(date_string, format_string)

with open("Library.xml") as fp:
	p = pl.readPlist(fp)
	print "Starting parse. Library contains", len(p["Tracks"]), "tracks,", len(p["Playlists"]), "playlists..."

	# clean playlists
	print "Cleaning playists..."
	for playlist in p["Playlists"]:
		try:
			playlist_length = len(playlist["Playlist Items"])
			new_playlist_name = str(playlist["Name"].lower().replace(" ", "_"))
			print "Playlist:", playlist["Name"], "- contains", playlist_length, "items"
			temp_playlist = []
			for item in playlist["Playlist Items"]:
				#check to see date added in lib
				track_key = item["Track ID"]
				if p["Tracks"][str(track_key)]["Date Added"] < cutoff:
					#print "Remove:", p["Tracks"][str(track_key)]["Name"]
					pass
				else:
					#copy to temp playlist
					temp_playlist.append(item)

			playlist["Playlist Items"] = temp_playlist
			playlist["Name"] = new_playlist_name
			print "New count:", len(playlist["Playlist Items"]), "items"
		except Exception as e:
			#print "Can't process playlist:", playlist["Name"], e
			pass

	print "...done."
	print "Cleaning songs..."
	# clean tracks
	for track in p["Tracks"].keys():
		track_key = p["Tracks"][track]
		#transform song name, remove (feat...) which messes up spotify search
		if "(" in track_key["Name"]:
			song_name = track_key["Name"]
			new_song_name = song_name.split("(")[0]
			p["Tracks"][track]["Name"] = new_song_name

		#remove multiple artists which messes up spotify search
		try:
			if "&" in track_key["Artist"]:
				artist_name = track_key["Artist"]
				new_artist_name = artist_name.split("&")[0]
				p["Tracks"][track]["Artist"] = new_artist_name

			if "," in track_key["Artist"]:
				artist_name = track_key["Artist"]
				new_artist_name = artist_name.split(",")[0]
				p["Tracks"][track]["Artist"] = new_artist_name
		except Exception as e:
			# Artist field doesn't exist
			#print "Can't process track:", track_key["Name"], e
			pass

		try:
			if track_key["Date Added"] < cutoff:
				#remove from tracks
				del(p["Tracks"][track])

		except:
			#remove from tracks
			del(p["Tracks"][track])

	with open("Library_parsed.xml", 'wb') as fn:
		pl.writePlist(p, fn)

	print "...done. New count:", len(p["Tracks"]), "tracks"