import { useState } from 'react'
import Header from './components/Header'
import TabNavigation from './components/TabNavigation'
import TopicBlogForm from './components/TopicBlogForm'
import YouTubeBlogForm from './components/YouTubeBlogForm'
import BlogPreview from './components/BlogPreview'
import Toast from './components/Toast'

function App() {
  const [activeTab, setActiveTab] = useState('topic')
  const [blog, setBlog] = useState(null)
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)

  const showToast = (message, type = 'success') => {
    setToast({ message, type })
    setTimeout(() => setToast(null), 3000)
  }

  const handleBlogGenerated = (blogData) => {
    setBlog(blogData)
    showToast('Blog generated successfully!', 'success')
  }

  const handleError = (error) => {
    showToast(error || 'An error occurred. Please try again.', 'error')
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 max-w-[1600px]">
        <div className="text-center mb-8 sm:mb-12 animate-fade-in-up">
          <h1 className="text-3xl sm:text-4xl lg:text-hero mb-3 sm:mb-4 text-neutral-text-primary font-bold">
            BlogGen AI
          </h1>
          <p className="text-base sm:text-lg text-neutral-text-secondary max-w-2xl mx-auto px-4">
            Generate professional, SEO-friendly blog posts from topics or YouTube videos
            using advanced AI technology
          </p>
        </div>

        <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />

        {/* Split Screen Layout */}
        <div className="mt-6 sm:mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8">
          {/* Left Side - Form */}
          <div className="lg:sticky lg:top-24 lg:self-start">
            <div 
              key={activeTab}
              className={activeTab === 'topic' ? 'animate-slide-in-left' : 'animate-slide-in-right'}
            >
              {activeTab === 'topic' ? (
                <TopicBlogForm
                  onBlogGenerated={handleBlogGenerated}
                  onError={handleError}
                  loading={loading}
                  setLoading={setLoading}
                />
              ) : (
                <YouTubeBlogForm
                  onBlogGenerated={handleBlogGenerated}
                  onError={handleError}
                  loading={loading}
                  setLoading={setLoading}
                />
              )}
            </div>
          </div>

          {/* Right Side - Preview */}
          <div className="min-h-[400px]">
            {blog ? (
              <div className="animate-fade-in-up">
                <BlogPreview blog={blog} />
              </div>
            ) : (
              <div className="card h-full flex items-center justify-center text-neutral-text-secondary">
                <div className="text-center">
                  <p className="text-lg mb-2">No blog generated yet</p>
                  <p className="text-sm">Fill out the form to generate your blog post</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-neutral-border py-6 sm:py-8 mt-12 sm:mt-16">
        <div className="container mx-auto px-4 text-center text-neutral-text-secondary text-sm sm:text-base">
          <p>© 2024 BlogGen AI | Made with ❤️</p>
        </div>
      </footer>

      {toast && <Toast message={toast.message} type={toast.type} />}
    </div>
  )
}

export default App

