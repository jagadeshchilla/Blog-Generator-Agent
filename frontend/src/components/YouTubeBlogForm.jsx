import { useState } from 'react'
import { Youtube, ArrowRight, Loader2, AlertCircle } from 'lucide-react'
import { generateBlogFromYouTube } from '../services/api'

const languages = [
  { value: 'english', label: 'English', flag: '🇬🇧' },
  { value: 'hindi', label: 'Hindi', flag: '🇮🇳' },
  { value: 'french', label: 'French', flag: '🇫🇷' },
  { value: 'telugu', label: 'Telugu', flag: '🇹🇼' },
  { value: 'tamil', label: 'Tamil', flag: '🇮🇳' },
  { value: 'malayalam', label: 'Malayalam', flag: '🇮🇳' },
  { value: 'japanese', label: 'Japanese', flag: '🇯🇵' },
  { value: 'chinese', label: 'Chinese', flag: '🇨🇳' },
]

const YouTubeBlogForm = ({ onBlogGenerated, onError, loading, setLoading }) => {
  const [url, setUrl] = useState('')
  const [language, setLanguage] = useState('english')
  const [urlError, setUrlError] = useState('')

  const validateYouTubeUrl = (url) => {
    const patterns = [
      /^https?:\/\/(www\.)?youtube\.com\/watch\?v=[\w-]+/,
      /^https?:\/\/youtu\.be\/[\w-]+/,
    ]
    return patterns.some((pattern) => pattern.test(url))
  }

  const handleUrlChange = (e) => {
    const value = e.target.value
    setUrl(value)
    
    if (value && !validateYouTubeUrl(value)) {
      setUrlError('Please enter a valid YouTube URL')
    } else {
      setUrlError('')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!url.trim()) {
      onError('Please enter a YouTube URL')
      return
    }
    
    if (!validateYouTubeUrl(url)) {
      setUrlError('Please enter a valid YouTube URL')
      return
    }

    setLoading(true)
    setUrlError('')
    try {
      const result = await generateBlogFromYouTube(url, language)
      onBlogGenerated(result)
      setUrl('') // Clear form after success
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || 'Failed to generate blog'
      onError(errorMessage)
      setUrlError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card animate-scale-in">
      <div className="flex items-center gap-3 mb-6">
        <Youtube className="w-5 h-5 sm:w-6 sm:h-6 text-primary flex-shrink-0" />
        <h2 className="text-xl sm:text-card-title text-neutral-text-primary">
          Generate Blog from YouTube Video
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="youtube-url" className="block text-sm font-medium text-neutral-text-primary mb-2">
            YouTube URL <span className="text-error">*</span>
          </label>
          <input
            id="youtube-url"
            type="url"
            value={url}
            onChange={handleUrlChange}
            placeholder="https://youtube.com/watch?v=... or https://youtu.be/..."
            className={`input-field ${urlError ? 'border-error focus:border-error focus:ring-error/10' : ''}`}
            disabled={loading}
            required
          />
          {urlError && (
            <div className="mt-2 flex items-center gap-2 text-error text-sm">
              <AlertCircle className="w-4 h-4" />
              <span>{urlError}</span>
            </div>
          )}
          <p className="mt-2 text-sm text-neutral-text-secondary flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            We'll extract the transcript and generate blog content
          </p>
        </div>

        <div>
          <label htmlFor="youtube-language" className="block text-sm font-medium text-neutral-text-primary mb-2">
            Language
          </label>
          <select
            id="youtube-language"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="input-field"
            disabled={loading}
          >
            {languages.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.flag} {lang.label}
              </option>
            ))}
          </select>
        </div>

        <button
          type="submit"
          className="btn-primary w-full justify-center"
          disabled={loading || !url.trim() || !!urlError}
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating Blog...
            </>
          ) : (
            <>
              Generate Blog
              <ArrowRight className="w-5 h-5" />
            </>
          )}
        </button>
      </form>

      {loading && (
        <div className="mt-6 pt-6 border-t border-neutral-border animate-fade-in">
          <div className="space-y-3 mb-4">
            <div className="flex items-center gap-3 text-neutral-text-secondary animate-slide-in-left" style={{ animationDelay: '0.1s' }}>
              <Loader2 className="w-5 h-5 animate-spin text-primary flex-shrink-0" />
              <p className="text-sm">Extracting transcript...</p>
            </div>
            <div className="flex items-center gap-3 text-neutral-text-secondary animate-slide-in-left" style={{ animationDelay: '0.2s' }}>
              <Loader2 className="w-5 h-5 animate-spin text-primary flex-shrink-0" />
              <p className="text-sm">Generating blog content...</p>
            </div>
            {language !== 'english' && (
              <div className="flex items-center gap-3 text-neutral-text-secondary animate-slide-in-left" style={{ animationDelay: '0.3s' }}>
                <Loader2 className="w-5 h-5 animate-spin text-primary flex-shrink-0" />
                <p className="text-sm">Translating to {languages.find(l => l.value === language)?.label}...</p>
              </div>
            )}
          </div>
          <div className="mt-4 h-1.5 bg-neutral-border rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-primary to-primary-light animate-progress rounded-full"></div>
          </div>
        </div>
      )}
    </div>
  )
}

export default YouTubeBlogForm

