from pytubefix import YouTube

urls = input("url:")

vid = YouTube(urls)

video_download = vid.streams.get_highest_resolution()
audio_download = vid.streams.get_audio_only()
print(audio_download)
entry = YouTube(urls).title

print(f"\nVideo found: {entry}\n")

print(f"Downloading Video...")
video_download.download(filename=f"{entry}.mp4")

print("Downloading Audio...")
audio_download.download(filename=f"{entry}.mp3")

print("Program Completed")
# https://youtu.be/ns4_FNtLD_s?si=Rm44ZCNebBjblBjShttps://youtu.be/ns4_FNtLD_s?si=Rm44ZCNebBjblBjS