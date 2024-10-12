import yt_dlp
import os

class YouTubeToWebM:
    def __init__(self):
        self.url = input("Enter YouTube music URL: ")
        self.youtube_to_webm(self.url)

    def youtube_to_webm(self, url):
        try:
            download_folder = os.getcwd()

            ydl_opts = {
                'format': 'bestaudio[ext=webm]',
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Download successful!")
            
            # Find the newly downloaded file
            files = os.listdir(download_folder)
            print(f"Files in directory: {files}")
            
            downloaded_file = max(files, key=lambda x: os.path.getctime(os.path.join(download_folder, x)))
            print(f"Downloaded file: {downloaded_file}")
            
            print(f"File saved as: {os.path.join(download_folder, downloaded_file)}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    YouTubeToWebM()