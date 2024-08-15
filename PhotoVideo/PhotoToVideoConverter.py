import os
import subprocess
from pathlib import Path

class PhotoToVideoConverter:
    def __init__(self, image_dir, output_video, ffmpeg_path='ffmpeg', frame_rate=60, resolution=(1920, 1080)):
        self.image_dir = Path(image_dir)
        self.output_video = output_video
        self.ffmpeg_path = ffmpeg_path
        self.frame_rate = frame_rate
        self.resolution = resolution
        self.file_list_path = 'file_list.txt'

    def _generate_file_list(self):
        """Generate a text file listing all .png image files in alphabetical order."""
        with open(self.file_list_path, 'w') as file_list:
            for image_file in sorted(self.image_dir.glob('*.png')):
                file_list.write(f"file '{image_file}'\n")

    def _convert_images_to_video(self):
        """Convert images to a video using ffmpeg."""
        ffmpeg_command = [
            self.ffmpeg_path,  # Full path if not in PATH
            '-hide_banner',  # Hide version and startup information
            '-y',  # Overwrite output file without asking
            '-r', str(self.frame_rate),
            '-f', 'concat',
            '-safe', '0',
            '-i', self.file_list_path,
            '-s', f'{self.resolution[0]}x{self.resolution[1]}',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            self.output_video
        ]
        try:
            subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True)
        except FileNotFoundError:
            print(f"Error: {self.ffmpeg_path} not found. Make sure ffmpeg is installed and the path is correct.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while creating the video: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def convert(self):
        """Generate the video from images."""
        try:
            self._generate_file_list()
            self._convert_images_to_video()
            os.remove(self.file_list_path)
            #print(f"Video '{self.output_video}' created successfully.")
        except Exception as e:
            print(f"An unexpected error occurred during the conversion process: {e}")
'''
# Example usage
image_dir = 'path to photos'
output_video = 'path to video output\output_video.mkv'
converter = PhotoToVideoConverter(image_dir, output_video, frame_rate=60)
converter.convert()
'''