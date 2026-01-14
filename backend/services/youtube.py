import yt_dlp
import os
from typing import Dict, Any, Optional

class YouTubeService:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'writeautomaticsub': True,
            'writesubtitles': True,
            'subtitleslangs': ['en', 'zh-Hans', 'zh-Hant'],
            'skip_download': True, # We only need metadata and subtitles for now
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        # Check for cookies.txt in current directory or backend directory
        cookie_file = "cookies.txt"
        if not os.path.exists(cookie_file):
            # Try looking in backend folder if running from root
            cookie_file = os.path.join("backend", "cookies.txt")
            
        if os.path.exists(cookie_file):
            print(f"Found cookie file at {cookie_file}, using it for authentication.")
            self.ydl_opts['cookiefile'] = cookie_file
        else:
            # Check for cookies in environment variable (for production/Vercel)
            cookies_content = os.getenv("YOUTUBE_COOKIES_CONTENT")
            if cookies_content:
                print("Found YOUTUBE_COOKIES_CONTENT env var, creating temp cookie file...")
                import tempfile
                # Create a temporary file to store cookies
                # We use delete=False because yt-dlp needs to read it by path
                # Ideally we should clean this up, but for serverless it's fine (ephemeral)
                try:
                    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as temp_cookie_file:
                        temp_cookie_file.write(cookies_content)
                        self.ydl_opts['cookiefile'] = temp_cookie_file.name
                        print(f"Created temp cookie file at {temp_cookie_file.name}")
                except Exception as e:
                    print(f"Failed to create temp cookie file: {e}")
            else:
                # Check for browser cookies (Local development convenience)
                browser_name = os.getenv("YOUTUBE_COOKIES_BROWSER")
                if browser_name:
                    print(f"YOUTUBE_COOKIES_BROWSER set to '{browser_name}', attempting to load cookies from browser...")
                    # Tuple format: (browser, profile, container, keyring) - usually just browser is enough
                    self.ydl_opts['cookiesfrombrowser'] = (browser_name,)
                else:
                    print("No cookies.txt, YOUTUBE_COOKIES_CONTENT, or YOUTUBE_COOKIES_BROWSER found.")
                    print("If you encounter 'Sign in' errors, please configure one of these authentication methods.")

    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Get video metadata and subtitle content.
        """
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Extract subtitles
                # Note: Actual subtitle downloading might require 'skip_download': False or specific API usage
                # For this MVP, we'll try to get the automatic captions url if available
                
                subtitles = ""
                # Logic to fetch subtitle text would go here. 
                # Since yt-dlp extract_info doesn't return full subtitle text directly, 
                # we might need to download it or use a separate library like youtube-transcript-api for easier text access.
                # For robustness, let's use a placeholder or integrate youtube-transcript-api if available.
                
                return {
                    "title": info.get('title'),
                    "channel": info.get('uploader'),
                    "duration": info.get('duration'),
                    "upload_date": info.get('upload_date'),
                    "thumbnail": info.get('thumbnail'),
                    "view_count": info.get('view_count'),
                    "description": info.get('description'),
                    "chapters": info.get('chapters', []),
                    "raw_info": info
                }
        except Exception as e:
            raise Exception(f"Error fetching video info: {str(e)}")

    def get_transcript(self, url: str) -> str:
        """
        Fetch transcript text. 
        For MVP, we will try to use youtube_transcript_api if installed, otherwise fallback.
        """
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            import re
            
            # Robust video ID extraction
            video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
            if not video_id_match:
                raise ValueError("Could not extract video ID from URL")
            
            video_id = video_id_match.group(1)
            print(f"Extracted video ID: {video_id}")
            
            try:
                # Use list_transcripts to get all available transcripts (manual and auto-generated)
                print("Fetching transcript list...")
                transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                
                transcript = None
                
                # Try to find manually created transcripts first
                try:
                    transcript = transcript_list.find_manually_created_transcript(['zh-Hans', 'zh-CN', 'zh-TW', 'zh-HK', 'en'])
                    print(f"Found manual transcript: {transcript.language_code}")
                except Exception:
                    # If no manual transcript, try generated ones
                    try:
                        transcript = transcript_list.find_generated_transcript(['zh-Hans', 'zh-CN', 'zh-TW', 'zh-HK', 'en'])
                        print(f"Found generated transcript: {transcript.language_code}")
                    except Exception:
                        # If specific languages not found, take the first available one and translate
                        print("No target language found, taking first available and translating...")
                        first_transcript = next(iter(transcript_list))
                        if first_transcript:
                            transcript = first_transcript.translate('zh-Hans')
                            print(f"Translated transcript from {first_transcript.language_code} to zh-Hans")

                if not transcript:
                    raise ValueError("No suitable transcript found.")

                # Fetch the actual data
                transcript_data = transcript.fetch()
                full_text = " ".join([item['text'] for item in transcript_data])
                print(f"Transcript fetched successfully (length: {len(full_text)})")
                return full_text

            except Exception as e:
                print(f"Detailed transcript fetch failed: {e}")
                # Fallback to Whisper ASR
                print("Attempting fallback to Audio Transcription (Whisper)...")
                try:
                    return self.transcribe_audio(url)
                except Exception as whisper_error:
                    print(f"Whisper transcription failed: {whisper_error}")
                    raise Exception(f"Could not retrieve transcript (Subtitles unavailable & Whisper failed): {str(e)} | {str(whisper_error)}")
                 
        except ImportError:
            raise ImportError("Transcript fetching requires youtube-transcript-api package. Please install it.")
        except Exception as e:
            print(f"Fatal error in get_transcript: {str(e)}")
            raise e

    def transcribe_audio(self, url: str) -> str:
        """
        Download audio and transcribe using OpenAI Whisper API or Local Whisper Model.
        """
        print("Starting audio download for transcription...")
        import uuid
        import glob
        
        # Unique prefix for temp file
        run_id = str(uuid.uuid4())
        temp_prefix = f"temp_audio_{run_id}"
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'outtmpl': temp_prefix, # yt-dlp will append .mp3
            'quiet': True,
        }
        
        downloaded_file = None
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find the file (it should be temp_prefix.mp3)
            possible_files = glob.glob(f"{temp_prefix}*")
            if not possible_files:
                raise Exception("Audio download failed: Output file not found.")
            
            downloaded_file = possible_files[0]
            print(f"Audio downloaded to {downloaded_file}.")
            
            # Check for API Key
            api_key = os.getenv("OPENAI_API_KEY")
            
            if api_key:
                print("Using OpenAI API for transcription...")
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                
                with open(downloaded_file, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file,
                        response_format="text"
                    )
                print("OpenAI API Transcription complete.")
                return transcription
            else:
                print("OPENAI_API_KEY not found. Attempting to use local Whisper model...")
                try:
                    import whisper
                    print("Loading local Whisper model (base)... this may take a moment.")
                    # Use 'base' or 'small' model for balance of speed and accuracy
                    model = whisper.load_model("base")
                    result = model.transcribe(downloaded_file)
                    print("Local Transcription complete.")
                    return result["text"]
                except ImportError:
                    raise Exception(
                        "Transcription failed: No OpenAI API Key found AND 'openai-whisper' package not installed.\n"
                        "Option 1: Add OPENAI_API_KEY to .env\n"
                        "Option 2: Install local whisper (Free): pip install openai-whisper torch"
                    )
                except Exception as local_e:
                    raise Exception(f"Local Whisper transcription failed: {local_e}")

        except Exception as e:
            print(f"Audio transcription process failed: {e}")
            raise e
        finally:
            # Cleanup
            if downloaded_file and os.path.exists(downloaded_file):
                try:
                    os.remove(downloaded_file)
                    print(f"Cleaned up temp file: {downloaded_file}")
                except Exception:
                    pass
