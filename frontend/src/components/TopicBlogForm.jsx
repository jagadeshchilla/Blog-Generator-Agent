import { useState } from 'react'
import { FileText, ArrowRight, Loader2 } from 'lucide-react'
import { generateBlogFromTopic } from '../services/api'

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

const TopicBlogForm = ({ onBlogGenerated, onError, loading, setLoading }) => {
  const [topic, setTopic] = useState('')
  const [language, setLanguage] = useState('english')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!topic.trim()) {
      onError('Please enter a topic')
      return
    }

    setLoading(true)
    try {
      const result = await generateBlogFromTopic(topic, language)
      onBlogGenerated(result)
      setTopic('') // Clear form after success
    } catch (error) {
      onError(error.response?.data?.detail || error.message || 'Failed to generate blog')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card animate-scale-in">
      <div className="flex items-center gap-3 mb-6">
        <FileText className="w-5 h-5 sm:w-6 sm:h-6 text-primary flex-shrink-0" />
        <h2 className="text-xl sm:text-card-title text-neutral-text-primary">
          Generate Blog from Topic
        </h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="topic" className="block text-sm font-medium text-neutral-text-primary mb-2">
            Topic <span className="text-error">*</span>
          </label>
          <input
            id="topic"
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="e.g., The Future of AI"
            className="input-field"
            disabled={loading}
            required
          />
        </div>

        <div>
          <label htmlFor="language" className="block text-sm font-medium text-neutral-text-primary mb-2">
            Language
          </label>
          <select
            id="language"
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
          disabled={loading || !topic.trim()}
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
          <div className="flex items-center gap-3 text-neutral-text-secondary mb-4">
            <Loader2 className="w-5 h-5 animate-spin text-primary flex-shrink-0" />
            <p className="text-sm">
              Generating your blog... This may take 30-60 seconds
            </p>
          </div>
          <div className="mt-4 h-1.5 bg-neutral-border rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-primary to-primary-light animate-progress rounded-full"></div>
          </div>
        </div>
      )}
    </div>
  )
}

export default TopicBlogForm

