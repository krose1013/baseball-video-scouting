import subprocess
import os

def trim_clip_ffmpeg(input_video_path, start_sec, end_sec, output_path):
    """
    Trims raw video file using FFmpeg stream copy (-c copy) for rapid slicing.
    """
    if not os.path.exists(input_video_path):
        return False, "Input video file not found."

    # Direct FFmpeg command execution
    cmd = [
        "ffmpeg",
        "-y",                     # Overwrite output without prompting
        "-ss", str(start_sec),    # Fast seek start time
        "-i", input_video_path,   # Input video
        "-to", str(end_sec),      # End time
        "-c", "copy",             # Codec copy (no re-encoding = instant processing)
        output_path
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True, output_path
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)