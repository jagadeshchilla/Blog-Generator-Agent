# Deployment Guide for YouTube Transcript Extraction

## Issue: YouTube Transcript Extraction on Vercel

YouTube often blocks requests from cloud provider IP addresses (like Vercel), which can cause transcript extraction to fail even when it works locally.

## Solutions

### Solution 1: Use YouTube Cookies (Recommended for Better Success Rate)

The code now supports using YouTube cookies to authenticate requests, which can help bypass IP blocking:

1. **Export cookies from your browser:**
   - Use a browser extension like "Get cookies.txt LOCALLY" or "Cookie-Editor"
   - Visit YouTube while logged in
   - Export cookies as a text file

2. **Add cookies to Vercel environment variables:**
   - Go to your Vercel project settings
   - Add environment variable `YOUTUBE_COOKIES_FILE` with the path to your cookies file (if uploading to Vercel)
   - OR use `YOUTUBE_COOKIES` with the browser name (e.g., `chrome`, `firefox`) if running locally

**Note:** Cookie files should not be committed to git for security reasons.

### Solution 2: Enhanced Error Handling (Already Implemented)

The code now includes:
- **Retry logic** with exponential backoff
- **Multiple methods** (youtube-transcript-api, yt-dlp, direct API)
- **Better headers** to reduce bot detection
- **Improved error messages** to help diagnose issues

### Solution 3: YouTube Data API v3 (Most Reliable for Production)

For production deployments, consider using YouTube Data API v3:

1. **Get a YouTube Data API key:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable YouTube Data API v3
   - Create credentials (API key)

2. **Update the code to use the API:**
   ```python
   # This would require modifying blog_node.py to use the official API
   # API endpoint: https://www.googleapis.com/youtube/v3/captions
   ```

3. **Add API key to Vercel:**
   - Add environment variable `YOUTUBE_API_KEY` in Vercel settings

## Current Implementation

The code tries three methods in order:

1. **youtube-transcript-api** - With retries and multiple language attempts
2. **yt-dlp** - With enhanced headers and cookie support
3. **Direct API call** - Fallback method using YouTube's timedtext API

## Troubleshooting

### Error: "Transcript not available for this video"
- The video may not have captions/subtitles enabled
- Try a different video that you know has captions

### Error: "YouTube is blocking requests"
- This indicates IP-based blocking from YouTube
- Try using Solution 1 (cookies) or Solution 3 (official API)
- For development, consider using a proxy service (not recommended for production)

### Testing Locally
1. Make sure you have all dependencies: `pip install -r requirements.txt`
2. Test with a video that has captions: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
3. Check the console logs for which method succeeded

## Environment Variables for Vercel

Optional environment variables you can add in Vercel:

```
YOUTUBE_COOKIES_FILE=/path/to/cookies.txt  # Path to cookies file (if stored in project)
YOUTUBE_COOKIES=chrome                     # Browser name for cookie extraction (local only)
```

## Next Steps

1. Deploy the updated code to Vercel
2. Test with a video that has captions
3. If still failing, consider implementing YouTube Data API v3 integration
4. Monitor logs in Vercel dashboard to see which method is being used

