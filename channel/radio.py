# myapp/radio.py
import tempfile
import os
import subprocess
import threading
import random
from pathlib import Path

class HLSRadio:
    MEDIA_ROOT = r"C:/Users/NevVaek/Documents/Django/code/youtube/media/audio/LofiSingle"   # adjust
    loop_path = os.path.join(MEDIA_ROOT, "radio/Timeline-1.mp4")
    playlist_dir = os.path.join(MEDIA_ROOT, "playlist")
    playlist_path = os.path.join(playlist_dir, "playlist.txt")
    live_dir = os.path.join(MEDIA_ROOT, "live")  # output HLS dir
    m3u8_path = os.path.join(live_dir, "stream.m3u8")

    _proc = None
    _lock = threading.Lock()

    @classmethod
    def _build_playlist(cls):
        audio_dir = Path(cls.MEDIA_ROOT)
        tracks = [p.name for p in audio_dir.iterdir() if p.suffix.lower() == ".m4a"]
        if not tracks:
            raise RuntimeError("No .m4a tracks found")
        random.shuffle(tracks)
        os.makedirs(cls.playlist_dir, exist_ok=True)
        # use helper logic to write safe paths
        with open(cls.playlist_path, "w", encoding="utf-8") as f:
            for t in tracks:
                p = os.path.join(cls.MEDIA_ROOT, t).replace("\\", "/")
                p = p.replace("'", "'\\''")
                f.write(f"file '{p}'\n")

    @classmethod
    def start(cls):
        """Start ffmpeg HLS writer if not running."""
        with cls._lock:
            if cls._proc and cls._proc.poll() is None:
                return cls._proc

            cls._build_playlist()
            os.makedirs(cls.live_dir, exist_ok=True)

            cmd = [
                "ffmpeg",
                "-hide_banner", "-loglevel", "warning",
                "-stream_loop", "-1", "-i", cls.loop_path,
                "-stream_loop", "-1", "-f", "concat", "-safe", "0", "-i", cls.playlist_path,
                "-map", "0:v:0", "-map", "1:a:0",
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "128k",
                "-f", "hls",
                "-hls_time", "4",
                "-hls_list_size", "6",
                "-hls_flags", "delete_segments+append_list+omit_endlist",
                "-hls_segment_filename", os.path.join(cls.live_dir, "%03d.ts"),cls.m3u8_path,
                "-hls_base_url", "/media/audio/LofiSingle/live/"
            ]

            proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            cls._proc = proc

            # optional: drain stderr so buffer doesn't grow
            threading.Thread(target=cls._drain_stderr, args=(proc,), daemon=True).start()
            return proc

    @classmethod
    def _drain_stderr(cls, proc):
        try:
            for line in iter(proc.stderr.readline, b''):
                if not line:
                    break
                # replace print with logging to file if desired
                print("[ffmpeg]", line.decode(errors="ignore").rstrip())
        except Exception:
            pass

    @classmethod
    def stop(cls):
        with cls._lock:
            if cls._proc:
                try:
                    cls._proc.terminate()
                    cls._proc.wait(timeout=3)
                except Exception:
                    try:
                        cls._proc.kill()
                    except Exception:
                        pass
                cls._proc = None


