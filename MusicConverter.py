import os
from moviepy import VideoFileClip
import subprocess

# Function to convert and speed up MP4 files
def convert_and_speed_up_video(video_file, speed_factor, output_dir):
    video = VideoFileClip(video_file)
    audio = video.audio
    # Save audio as a temporary MP3 file
    temp_audio_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(video_file))[0] + "_temp.mp3")
    audio.write_audiofile(temp_audio_filename, codec='libmp3lame')  # Use libmp3lame for MP3 export
    
    # Use sox for faster audio speed-up
    sped_up_audio_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(video_file))[0] + f".mp3")
    
    # Speed up the audio with sox
    subprocess.run([
        'sox', temp_audio_filename, sped_up_audio_filename,
        'tempo', str(speed_factor)
    ])
    
    # Clean up the temporary file
    os.remove(temp_audio_filename)
    
    video.close()
    audio.close()
    
    return sped_up_audio_filename

# Function to speed up MP3 files using sox
def speed_up_mp3(mp3_file, speed_factor, output_dir):
    # Use sox for faster audio speed-up
    sped_up_audio_filename = os.path.join(output_dir, os.path.splitext(os.path.basename(mp3_file))[0] + f".mp3")
    
    subprocess.run([
        'sox', mp3_file, sped_up_audio_filename,
        'tempo', str(speed_factor)
    ])
    
    return sped_up_audio_filename

# Function to process all video and audio files in a directory
def process_files_in_directory(directory, speed_factor, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all video and audio files in the directory
    files = [f for f in os.listdir(directory) if f.endswith(('.mp4', '.mp3', '.m4a', '.mkv'))]

    # Process each file
    for file in files:
        file_path = os.path.join(directory, file)
        
        print(f"Processing {file_path}...")

        # Check if the file is a video or audio and handle accordingly
        if file.endswith((".mp4", ".mkv")):
            # Convert video to sped-up audio and then to MP3
            sped_up_audio_file = convert_and_speed_up_video(file_path, speed_factor, output_dir)
            print(f"Speeded-up audio file created from video: {sped_up_audio_file}")
        elif file.endswith(".m4a") or file.endswith(".mp3"):
            # Speed up the existing MP3 file
            sped_up_audio_file = speed_up_mp3(file_path, speed_factor, output_dir)
            print(f"Speeded-up MP3 file created: {sped_up_audio_file}")

# Main function
def main():
    directory = "MP4"  # Change this to the directory containing your files
    speed_factor = float(input("Enter Speed: "))
    output_dir = "MP3"

    # Process the video and audio files in the directory
    process_files_in_directory(directory, speed_factor, output_dir)

if __name__ == "__main__":
    main()
