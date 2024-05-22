import subprocess
import sys
import os

def scale_video(ffmpeg_path, input_path, output_path):
    # Set the scale factor
    scale_factor = 0.76

    # Calculate the padding values
    input_width = 1920
    output_width = int(input_width * scale_factor)
    pad_left = (input_width - output_width) // 2

    # ffmpeg command to scale the video
    command = [
        ffmpeg_path,
        '-i', input_path,
        '-vf', f"scale={output_width}:1080,pad=1920:1080:{pad_left}:0,setsar=1",
        '-r', '60',  # Set the frame rate to 60fps
        '-c:a', 'copy',  # Copy the audio without re-encoding
        '-y',  # Overwrite the output file if it exists
        output_path
    ]

    # Execute the command
    subprocess.run(command, check=True)

def process_videos_in_folder(ffmpeg_path, input_folder, output_folder):
    if not os.path.isdir(input_folder):
        print(f"Input folder not found: {input_folder}")
        sys.exit(1)

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".mp4"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                scale_video(ffmpeg_path, input_path, output_path)
                print(f"Processed video: {filename}")
            except subprocess.CalledProcessError as e:
                print(f"An error occurred while processing {filename}: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python scale_video.py <ffmpeg_path> <input_folder> <output_folder>")
        sys.exit(1)

    ffmpeg_path = sys.argv[1]
    input_folder = sys.argv[2]
    output_folder = sys.argv[3]

    if not os.path.isfile(ffmpeg_path):
        print(f"ffmpeg executable not found at {ffmpeg_path}")
        sys.exit(1)

    process_videos_in_folder(ffmpeg_path, input_folder, output_folder)
