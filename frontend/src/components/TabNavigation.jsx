import { FileText, Youtube } from 'lucide-react'

const TabNavigation = ({ activeTab, onTabChange }) => {
  return (
    <div className="flex gap-2 sm:gap-4 border-b border-neutral-border overflow-x-auto scrollbar-hide">
      <button
        onClick={() => onTabChange('topic')}
        className={`tab-button flex items-center gap-2 whitespace-nowrap ${
          activeTab === 'topic' ? 'active' : ''
        }`}
      >
        <FileText className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" />
        <span className="hidden xs:inline">Topic Blog</span>
        <span className="xs:hidden">Topic</span>
      </button>
      <button
        onClick={() => onTabChange('youtube')}
        className={`tab-button flex items-center gap-2 whitespace-nowrap ${
          activeTab === 'youtube' ? 'active' : ''
        }`}
      >
        <Youtube className="w-4 h-4 sm:w-5 sm:h-5 flex-shrink-0" />
        <span className="hidden xs:inline">YouTube Blog</span>
        <span className="xs:hidden">YouTube</span>
      </button>
    </div>
  )
}

export default TabNavigation

