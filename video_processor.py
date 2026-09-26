import os
import subprocess

def extract_audio(video_path: str, output_audio_path: str) -> bool:
    """
    Extracts the audio track from a video file and saves it as an MP3.
    """
    try:
        command = [
            "ffmpeg",
            "-i", video_path,
            "-q:a", "0",
            "-map", "a",
            output_audio_path,
            "-y" # Overwrite output files without asking
        ]
        
        # Run ffmpeg command
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error during audio extraction: {e.stderr.decode('utf-8')}")
        return False
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in system PATH.")
        return False

def extract_keyframes(video_path: str, output_dir: str, fps: int = 1) -> list:
    """
    Extracts frames from a video at a specified frame rate (default 1 fps) to avoid processing every frame.
    Returns a list of extracted frame file paths.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        command = [
            "ffmpeg",
            "-i", video_path,
            "-vf", f"fps={fps}",
            os.path.join(output_dir, "frame_%04d.jpg"),
            "-y"
        ]
        
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Get list of extracted frames
        frames = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".jpg")]
        return sorted(frames)
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error during frame extraction: {e.stderr.decode('utf-8')}")
        return []
    except FileNotFoundError:
        print("FFmpeg is not installed or not found in system PATH.")
        return []
