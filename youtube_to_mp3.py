import av
import yt_dlp
import os
import time

class YouTubeToMP3:
    def __init__(self):
        self.url = input("Enter YouTube music URL: ")
        self.youtube_to_mp3(self.url)

    def youtube_to_mp3(self, url):
        try:
            download_folder = os.getcwd()
            ydl_opts = {
                'format': 'bestaudio[ext=webm]/bestaudio',
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Download successful!")

            # Find the newly downloaded file
            files = os.listdir(download_folder)
            downloaded_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_folder, x)))

            # Convert WebM to high-quality MP3
            webm_file = os.path.join(download_folder, downloaded_file)
            mp3_file = os.path.join(download_folder, downloaded_file.replace('.webm', '.mp3'))
            with av.open(webm_file) as input_container:
                stream = input_container.streams.audio[0]
                
                with av.open(mp3_file, mode='w') as output_container:
                    ostream = output_container.add_stream("mp3", rate=44100)
                    for packet in input_container.demux(stream):
                        for frame in packet.decode():
                            new_packets = ostream.encode(frame)
                            if new_packets:
                                output_container.mux(new_packets)
                    # Flush the encoder
                    try:
                        new_packets = ostream.encode(None)
                        while new_packets:
                            output_container.mux(new_packets)
                            new_packets = ostream.encode(None)
                    except Exception as e:
                        if "End of file" in str(e):
                            print("Conversion completed successfully.")
                        else:
                            print(f"Error: {str(e)}")
            print(f"Conversion successful! High-quality MP3 file saved as: {mp3_file}")

            # Delete WebM file
            time.sleep(1)  # Wait for 1 second
            os.remove(webm_file)

        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    YouTubeToMP3()