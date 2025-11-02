import { useState } from 'react'
import { Copy, Download, Share2, Check, Globe } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

const BlogPreview = ({ blog }) => {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    const content = `# ${blog.title}\n\n${blog.content}`
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const handleDownload = () => {
    const content = `# ${blog.title}\n\n${blog.content}`
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${blog.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: blog.title,
          text: blog.content.substring(0, 200),
        })
      } catch (err) {
        console.error('Error sharing:', err)
      }
    } else {
      // Fallback: copy to clipboard
      handleCopy()
    }
  }

  const getLanguageLabel = () => {
    // Extract language from blog data if available
    return blog.language || 'English'
  }

  const getThumbnailUrl = (videoId) => {
    if (!videoId) return null
    return `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`
  }

  return (
    <div className="card animate-bounce-in">
      {/* YouTube Thumbnail */}
      {blog.videoId && (
        <div className="mb-4 sm:mb-6 rounded-lg overflow-hidden animate-fade-in shadow-medium">
          <a 
            href={`https://www.youtube.com/watch?v=${blog.videoId}`}
            target="_blank"
            rel="noopener noreferrer"
            className="block relative group"
          >
            <img 
              src={getThumbnailUrl(blog.videoId)} 
              alt="YouTube Video Thumbnail"
              className="w-full h-auto max-w-full object-cover rounded-lg transition-transform duration-300 group-hover:scale-[1.02]"
              loading="lazy"
              onError={(e) => {
                // Fallback to standard quality if maxresdefault fails
                e.target.src = `https://img.youtube.com/vi/${blog.videoId}/hqdefault.jpg`
              }}
            />
            <div className="absolute inset-0 flex items-center justify-center bg-black/20 group-hover:bg-black/30 transition-colors rounded-lg">
              <div className="bg-red-600 rounded-full p-3 sm:p-4 group-hover:scale-110 transition-transform">
                <svg 
                  className="w-8 h-8 sm:w-12 sm:h-12 text-white" 
                  fill="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </div>
            </div>
          </a>
        </div>
      )}

      <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between mb-6 pb-6 border-b border-neutral-border gap-4">
        <div className="flex-1">
          <h2 className="text-2xl sm:text-3xl font-semibold text-primary mb-3 break-words">
            {blog.title}
          </h2>
          <div className="flex items-center gap-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-neutral-surface text-neutral-text-secondary text-xs sm:text-sm animate-scale-in">
              <Globe className="w-3 h-3 sm:w-4 sm:h-4" />
              {getLanguageLabel()}
            </span>
          </div>
        </div>
      </div>

      <div className="prose prose-sm sm:prose-base md:prose-lg max-w-none markdown-content mb-6 sm:mb-8 animate-fade-in" style={{ animationDelay: '0.2s' }}>
        <ReactMarkdown
          components={{
            // Responsive images
            img({ node, ...props }) {
              return (
                <span className="block my-4 w-full overflow-hidden rounded-lg">
                  <img 
                    {...props} 
                    className="w-full h-auto max-w-full object-contain rounded-lg shadow-small hover:shadow-medium transition-shadow"
                    loading="lazy"
                    alt={props.alt || 'Image'}
                  />
                </span>
              )
            },
            // Responsive tables with horizontal scroll on smaller screens
            table({ node, ...props }) {
              return (
                <div className="my-6 overflow-x-auto -mx-2 sm:-mx-4 md:mx-0">
                  <div className="inline-block min-w-full align-middle">
                    <div className="overflow-hidden shadow-small rounded-lg border border-neutral-border">
                      <table 
                        {...props} 
                        className="min-w-full divide-y divide-neutral-border"
                      />
                    </div>
                  </div>
                </div>
              )
            },
            // Table header cells
            th({ node, ...props }) {
              return (
                <th 
                  {...props} 
                  className="px-4 py-3 sm:px-6 sm:py-4 text-left text-xs sm:text-sm font-semibold text-neutral-text-primary uppercase tracking-wider bg-neutral-surface border-b border-neutral-border"
                />
              )
            },
            // Table body cells
            td({ node, ...props }) {
              return (
                <td 
                  {...props} 
                  className="px-4 py-3 sm:px-6 sm:py-4 text-xs sm:text-sm text-neutral-text-primary whitespace-nowrap sm:whitespace-normal border-b border-neutral-border"
                />
              )
            },
            // Code blocks
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || '')
              return !inline && match ? (
                <div className="my-4 overflow-x-auto -mx-2 sm:-mx-4 md:mx-0">
                  <div className="inline-block min-w-full">
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                      className="rounded-md text-xs sm:text-sm"
                      customStyle={{
                        margin: 0,
                        borderRadius: '8px',
                      }}
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  </div>
                </div>
              ) : (
                <code className={`${className || ''} text-xs sm:text-sm`} {...props}>
                  {children}
                </code>
              )
            },
            // Responsive pre blocks
            pre({ node, ...props }) {
              return (
                <div className="my-4 overflow-x-auto -mx-2 sm:-mx-4 md:mx-0">
                  <pre 
                    {...props} 
                    className="px-4 py-3 sm:px-6 sm:py-4 text-xs sm:text-sm rounded-lg overflow-x-auto"
                  />
                </div>
              )
            },
          }}
        >
          {blog.content}
        </ReactMarkdown>
      </div>

      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4 pt-6 border-t border-neutral-border">
        <button
          onClick={handleCopy}
          className={`btn-secondary ${copied ? 'bg-success border-success text-white' : ''} transition-all duration-normal`}
          aria-label="Copy blog content"
        >
          {copied ? (
            <>
              <Check className="w-4 h-4 sm:w-5 sm:h-5 animate-bounce-in" />
              Copied!
            </>
          ) : (
            <>
              <Copy className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="hidden sm:inline">Copy</span>
              <span className="sm:hidden">Copy</span>
            </>
          )}
        </button>
        <button
          onClick={handleDownload}
          className="btn-secondary"
          aria-label="Download as Markdown"
        >
          <Download className="w-4 h-4 sm:w-5 sm:h-5" />
          <span className="hidden sm:inline">Download MD</span>
          <span className="sm:hidden">Download</span>
        </button>
        <button
          onClick={handleShare}
          className="btn-secondary"
          aria-label="Share blog"
        >
          <Share2 className="w-4 h-4 sm:w-5 sm:h-5" />
          <span className="hidden sm:inline">Share</span>
          <span className="sm:hidden">Share</span>
        </button>
      </div>
    </div>
  )
}

export default BlogPreview

