import os
import subprocess

class VideoToImageExtractor:
    def __init__(self, video_file, output_dir, frame_rate=60):
        self.video_file = video_file
        self.output_dir = output_dir
        self.frame_rate = frame_rate

        # Ensure the output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def _escape_path(self, path):
        """Escape backslashes in Windows paths and quote the path."""
        return path.replace('\\', '/').replace('"', '\\"')

    def _extract_frames(self):
        escaped_video_file = self._escape_path(self.video_file)
        escaped_output_dir = self._escape_path(self.output_dir)
        # Use '%d' for frame numbering starting at 0
        frame_pattern = os.path.join(escaped_output_dir, 'encrypted_image_%d.png')

        ffmpeg_command = [
            'ffmpeg',
            '-hide_banner',  # Hide version and startup information
            '-y',  # Overwrite output file without asking
            '-i', escaped_video_file,
            '-vf', f'fps={self.frame_rate}',  # Extract frames at the specified frame rate
            '-start_number', '0',  # Start numbering from 0
            frame_pattern  # Save frames as PNG files
        ]
        
        # Run the command and capture output
        try:
            result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print(result.stdout)  # Print standard output if needed
        except FileNotFoundError:
            print(f"Error: ffmpeg not found. Make sure ffmpeg is installed and the path is correct.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while extracting frames: {e}")
            print(f"Error output: {e.stderr}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def extract(self):
        try:
            self._extract_frames()
            print(f"Frames extracted and saved to {self.output_dir}")
        except Exception as e:
            print(f"An unexpected error occurred during the extraction process: {e}")


'''# Example usage
if __name__ == "__main__":
    video_file = r'test file.mkv'
    output_dir = r'C:\Desktop\somepath\photos'
    extractor = VideoToImageExtractor(video_file, output_dir)
    extractor.extract()'''
