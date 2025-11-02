import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const generateBlogFromTopic = async (topic, language = 'english') => {
  try {
    const response = await api.post('/blogs/topic', {
      topic,
      language,
    })
    
    // Extract blog data from response
    // Response structure: { data: { blog: { title: "...", content: "..." } } }
    const data = response.data?.data || response.data
    const blog = data?.blog || data
    
    if (blog) {
      // Handle both string and object formats
      const title = typeof blog.title === 'string' ? blog.title : blog.title?.content || 'Untitled'
      const content = typeof blog.content === 'string' ? blog.content : blog.content?.content || ''
      
      return {
        title: title || 'Untitled',
        content: content || '',
        language: language,
        videoId: null, // Topic blogs don't have video IDs
      }
    }
    throw new Error('Invalid response format')
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data?.detail || 'Failed to generate blog')
    }
    throw error
  }
}

export const generateBlogFromYouTube = async (youtubeUrl, language = 'english') => {
  try {
    const response = await api.post('/blogs/youtube', {
      youtube_url: youtubeUrl,
      language,
    })
    
    // Extract blog data from response
    // Response structure: { data: { blog: { title: "...", content: "..." } }, video_id: "..." }
    const data = response.data?.data || response.data
    const blog = data?.blog || data
    // Extract video_id from response (can be at root level or in data)
    const videoId = response.data?.video_id || data?.video_id || null
    
    if (blog) {
      // Handle both string and object formats
      const title = typeof blog.title === 'string' ? blog.title : blog.title?.content || 'Untitled'
      const content = typeof blog.content === 'string' ? blog.content : blog.content?.content || ''
      
      return {
        title: title || 'Untitled',
        content: content || '',
        language: language,
        videoId: videoId, // Include video ID for thumbnail
      }
    }
    throw new Error('Invalid response format')
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data?.detail || 'Failed to generate blog')
    }
    throw error
  }
}

