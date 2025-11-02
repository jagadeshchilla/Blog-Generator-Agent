from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog
from youtube_transcript_api import YouTubeTranscriptApi

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
        Extract transcript from YouTube URL.
        """
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
            
            # Get transcript using the new API (v1.2.0+)
            ytt_api = YouTubeTranscriptApi()
            transcript = ytt_api.fetch(video_id)
            transcript_data = transcript.to_raw_data()
            transcript_text = " ".join([item['text'] for item in transcript_data])
            
            return {"transcript": transcript_text, "video_id": video_id}
        except ValueError:
            # Re-raise ValueError as-is (e.g., invalid URL format)
            raise
        except Exception as e:
            error_msg = str(e).lower()
            # Check for network-related errors
            if "nameresolutionerror" in error_msg or "failed to resolve" in error_msg or "getaddrinfo failed" in error_msg:
                raise ValueError("Network error: Cannot connect to YouTube. Please check your internet connection and DNS settings.")
            elif "connection" in error_msg and "failed" in error_msg:
                raise ValueError("Network error: Cannot connect to YouTube. Please check your internet connection.")
            elif "transcript" in error_msg and "not available" in error_msg:
                raise ValueError("Transcript not available for this video. The video may not have subtitles/transcripts enabled.")
            else:
                raise ValueError(f"Failed to extract transcript: {str(e)}")
    
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