from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog
import re

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly.
                   Return only the title, nothing else.

                   """
            
            system_message=prompt.format(topic=state["topic"])
            response=self.llm.invoke(system_message)
            
            # Safely extract content from response
            title = None
            if hasattr(response, 'content'):
                title = response.content
            elif isinstance(response, str):
                title = response
            else:
                title = str(response)
            
            # Strip any markdown formatting that might be in the title
            title = title.strip().strip('#').strip()
            
            return {"blog":{"title":title}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            
            # Safely extract title from state
            blog_title = None
            if "blog" in state and state["blog"]:
                if isinstance(state["blog"], dict):
                    blog_title = state["blog"].get("title", "Untitled")
                elif hasattr(state["blog"], "title"):
                    blog_title = state["blog"].title
                else:
                    blog_title = "Untitled"
            else:
                blog_title = "Untitled"
            
            # Safely extract content from response
            content = None
            if hasattr(response, 'content'):
                content = response.content
            elif isinstance(response, str):
                content = response
            else:
                content = str(response)
            
            return {"blog": {"title": blog_title, "content": content}}
        
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        """
        current_language = state.get("current_language", "english")
        blog_content = state["blog"]["content"]
        blog_title = state["blog"]["title"]
        
        translation_prompt="""
        Translate the following blog title and content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.
        - Keep the Markdown formatting intact.

        BLOG TITLE:
        {blog_title}

        ORIGINAL CONTENT:
        {blog_content}

        Return both the translated title and content maintaining the same structure.
        """
        # Translating to target language
        messages=[
            HumanMessage(translation_prompt.format(
                current_language=current_language, 
                blog_title=blog_title,
                blog_content=blog_content
            ))
        ]
        try:
            # Try structured output first
            translation_result = self.llm.with_structured_output(Blog).invoke(messages)
            return {
                "blog": {
                    "title": translation_result.title,
                    "content": translation_result.content
                }
            }
        except Exception as e:
            # Fallback to regular invoke if structured output fails
            # Structured output failed, using regular invoke
            response = self.llm.invoke(messages)
            # Assume the response contains both title and content
            return {
                "blog": {
                    "title": blog_title,  # Keep original title if translation fails
                    "content": response.content if hasattr(response, 'content') else str(response)
                }
            }

    def route(self, state: BlogState):
        """
        Route function to pass language information for translation decision.
        """
        current_language = state.get("current_language", "english")
        return {"current_language": current_language}
    

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        """
        supported_languages = ["hindi", "french", "telugu", "tamil", "malayalam", "english", "japanese", "chinese"]
        language = state.get("current_language", "english").lower()
        
        if language == "english":
            return "end"
        elif language in supported_languages:
            return "translate"
        else:
            return "translate"
    
    def extract_youtube_transcript(self, state: BlogState):
        """
        Extract transcript from YouTube URL using multiple methods with improved cloud compatibility.
        """
        import os
        import time
        
        youtube_url = state.get("youtube_url", "")
        if not youtube_url:
            raise ValueError("YouTube URL is required")
        
        try:
            # Extract video ID from URL
            video_id = None
            if "youtube.com/watch?v=" in youtube_url:
                video_id = youtube_url.split("v=")[1].split("&")[0]
            elif "youtu.be/" in youtube_url:
                video_id = youtube_url.split("youtu.be/")[1].split("?")[0]
            
            if not video_id:
                raise ValueError("Invalid YouTube URL format")
            
            transcript_text = None
            errors = []
            
            # Method 1: Try youtube-transcript-api with retries
            print(f"[1/3] Attempting youtube-transcript-api for video_id: {video_id}")
            for attempt in range(3):
                try:
                    from youtube_transcript_api import YouTubeTranscriptApi
                    
                    # Try with different language preferences
                    lang_attempts = [
                        ['en', 'en-US', 'en-GB'],
                        ['en'],
                        None  # Try any available language
                    ]
                    
                    for langs in lang_attempts:
                        try:
                            if langs is None:
                                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                            else:
                                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
                            
                            transcript_text = " ".join([item['text'] for item in transcript_list])
                            print(f"[SUCCESS] Got transcript via youtube-transcript-api, length: {len(transcript_text)}")
                            return {"transcript": transcript_text, "video_id": video_id}
                        except Exception as lang_e:
                            if attempt < len(lang_attempts) - 1:
                                continue
                            raise lang_e
                    
                except Exception as e:
                    error_str = str(e).lower()
                    if attempt < 2:  # Retry if not last attempt
                        wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s
                        print(f"[RETRY] Attempt {attempt + 1} failed, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    
                    ytt_error = str(e)
                    errors.append(f"youtube-transcript-api: {ytt_error}")
                    print(f"[FAILED] youtube-transcript-api error: {ytt_error}")
            
            # Method 2: Try yt-dlp with enhanced configuration
            print(f"[2/3] Attempting yt-dlp for video: {youtube_url}")
            try:
                import yt_dlp
                
                # Get cookies from environment if available
                cookies_file = os.getenv('YOUTUBE_COOKIES_FILE')
                cookies_from_browser = os.getenv('YOUTUBE_COOKIES')
                
                # Enhanced yt-dlp options for cloud environments
                ydl_opts = {
                    'skip_download': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU'],
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                    # Enhanced headers to avoid bot detection
                    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'referer': 'https://www.youtube.com/',
                    'cookiefile': cookies_file if cookies_file else None,
                    'cookiesfrombrowser': cookies_from_browser if cookies_from_browser else None,
                    # Additional options to reduce bot detection
                    'extractor_args': {
                        'youtube': {
                            'player_client': ['web', 'android'],  # Try web client first, fallback to android
                            'player_skip': ['webpage', 'configs'],
                        }
                    },
                    # Timeout settings
                    'socket_timeout': 30,
                    'http_chunk_size': 10485760,
                }
                
                # Remove None values from options
                ydl_opts = {k: v for k, v in ydl_opts.items() if v is not None}
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Get video info with retry
                    info = None
                    for attempt in range(2):
                        try:
                            info = ydl.extract_info(youtube_url, download=False)
                            break
                        except Exception as e:
                            if attempt == 0:
                                print(f"[RETRY] yt-dlp extract_info attempt {attempt + 1} failed, retrying...")
                                time.sleep(2)
                            else:
                                raise
                    
                    if not info:
                        raise ValueError("Failed to extract video info")
                    
                    # Try to get subtitles from info
                    subtitles = info.get('subtitles', {}) or info.get('automatic_captions', {})
                    print(f"yt-dlp found subtitles: {bool(subtitles)}")
                    
                    if subtitles:
                        # Try English subtitles first, then any available
                        en_subs = None
                        for lang_code in ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']:
                            if lang_code in subtitles:
                                en_subs = subtitles[lang_code]
                                break
                        
                        if not en_subs:
                            # Try any available language
                            all_subs = list(subtitles.values())
                            en_subs = all_subs[0] if all_subs else []
                        
                        if en_subs and len(en_subs) > 0:
                            sub_url = en_subs[0].get('url', '')
                            if not sub_url:
                                print("Subtitle URL not found")
                            else:
                                print(f"Downloading subtitle from URL: {sub_url[:50]}...")
                                # Download subtitle content with proper headers
                                import urllib.request
                                req = urllib.request.Request(
                                    sub_url,
                                    headers={
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                                        'Referer': 'https://www.youtube.com/',
                                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                        'Accept-Language': 'en-US,en;q=0.9',
                                    }
                                )
                                sub_response = urllib.request.urlopen(req, timeout=15)
                                sub_data = sub_response.read().decode('utf-8')
                                
                                # Parse subtitle format
                                transcript_text = self._parse_subtitle(sub_data)
                                if transcript_text and len(transcript_text.strip()) > 0:
                                    print(f"[SUCCESS] Got transcript via yt-dlp, length: {len(transcript_text)}")
                                    return {"transcript": transcript_text, "video_id": video_id}
                        else:
                            print("No subtitle entries found in subtitles dict")
                    else:
                        print("No subtitles found in video info")
                            
            except ImportError as e:
                yt_dlp_error = f"yt-dlp not installed: {str(e)}"
                errors.append(yt_dlp_error)
                print(f"[FAILED] {yt_dlp_error}")
            except Exception as e:
                yt_dlp_error = str(e)
                errors.append(f"yt-dlp: {yt_dlp_error}")
                print(f"[FAILED] yt-dlp error: {yt_dlp_error}")
            
            # Method 3: Try direct API call with enhanced headers (fallback)
            print(f"[3/3] Attempting direct API call for video_id: {video_id}")
            try:
                import urllib.request
                import json
                
                # Try to get transcript via YouTube's internal API
                api_url = f"https://www.youtube.com/api/timedtext?lang=en&v={video_id}"
                req = urllib.request.Request(
                    api_url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Referer': 'https://www.youtube.com/',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Origin': 'https://www.youtube.com',
                    }
                )
                
                response = urllib.request.urlopen(req, timeout=15)
                subtitle_data = response.read().decode('utf-8')
                transcript_text = self._parse_subtitle(subtitle_data)
                
                if transcript_text and len(transcript_text.strip()) > 0:
                    print(f"[SUCCESS] Got transcript via direct API, length: {len(transcript_text)}")
                    return {"transcript": transcript_text, "video_id": video_id}
            except Exception as e:
                api_error = str(e)
                errors.append(f"direct-api: {api_error}")
                print(f"[FAILED] Direct API error: {api_error}")
            
            # All methods failed
            error_msg = "Failed to extract transcript. "
            
            # Check for specific error patterns
            all_errors = " ".join(errors).lower()
            if any(keyword in all_errors for keyword in ["transcript", "not available", "no transcript"]):
                error_msg += "Transcript not available for this video. The video may not have subtitles/transcripts enabled."
            elif any(keyword in all_errors for keyword in ["blocking", "ip", "cloud", "bot", "sign in", "403", "429"]):
                error_msg += "YouTube is blocking requests from this server (likely IP-based blocking in cloud environment). "
                error_msg += "This is a known issue with cloud providers. Consider using YouTube Data API v3 with an API key for production."
            else:
                error_msg += "Methods attempted: " + "; ".join(errors) if errors else "No methods available"
            
            raise ValueError(error_msg)
                
        except ValueError:
            raise
        except Exception as e:
            error_msg = str(e).lower()
            if "transcript" in error_msg and "not available" in error_msg:
                raise ValueError("Transcript not available for this video. The video may not have subtitles/transcripts enabled.")
            else:
                raise ValueError(f"Failed to extract transcript: {str(e)}")
    
    def _parse_subtitle(self, subtitle_data: str) -> str:
        """Parse VTT or SRT subtitle format and extract text."""
        lines = subtitle_data.split('\n')
        transcript_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip VTT/SRT timestamps and formatting
            if not line or line.startswith('WEBVTT') or line.startswith('Kind:') or '-->' in line:
                continue
            # Skip sequence numbers in SRT
            if line.isdigit():
                continue
            # Remove HTML tags if present
            line = re.sub(r'<[^>]+>', '', line)
            if line:
                transcript_lines.append(line)
        
        return " ".join(transcript_lines)
    
    def generate_blog_from_transcript(self, state: BlogState):
        """
        Generate blog title and content from YouTube transcript.
        """
        transcript = state.get("transcript", "")
        if not transcript:
            raise ValueError("Transcript is required")
        
        # Generate title from transcript
        title_prompt = """
        You are an expert blog content writer. Use Markdown formatting.
        Based on the following YouTube video transcript, generate a creative and SEO-friendly blog title.
        
        TRANSCRIPT:
        {transcript}
        
        Generate only the title, nothing else.
        """
        
        title_message = title_prompt.format(transcript=transcript[:2000])
        title_response = self.llm.invoke(title_message)
        
        # Extract title safely
        title = None
        if hasattr(title_response, 'content'):
            title = title_response.content
        elif isinstance(title_response, str):
            title = title_response
        else:
            title = str(title_response)
        title = title.strip().strip('#').strip()
        
        # Generate blog content from transcript
        content_prompt = """You are an expert blog writer. Use Markdown formatting.
        Based on the following YouTube video transcript, generate a detailed, well-structured blog post.
        - Create engaging content with proper headings, subheadings, and formatting
        - Summarize key points from the transcript
        - Make it readable and informative
        - Use Markdown formatting
        
        TRANSCRIPT:
        {transcript}
        """
        
        content_message = content_prompt.format(transcript=transcript)
        content_response = self.llm.invoke(content_message)
        
        # Extract content safely
        content = None
        if hasattr(content_response, 'content'):
            content = content_response.content
        elif isinstance(content_response, str):
            content = content_response
        else:
            content = str(content_response)
        
        return {
            "blog": {
                "title": title,
                "content": content
            }
        }