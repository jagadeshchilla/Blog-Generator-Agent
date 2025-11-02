import { FileText } from 'lucide-react'

const Header = () => {
  return (
    <header className="bg-white shadow-small sticky top-0 z-50 transition-all duration-normal backdrop-blur-sm bg-white/95">
      <div className="container mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16 sm:h-18">
          <div className="flex items-center gap-2 sm:gap-3 animate-slide-in-left">
            <FileText className="w-6 h-6 sm:w-7 sm:h-7 text-primary flex-shrink-0" />
            <span className="text-lg sm:text-xl font-bold text-neutral-text-primary">
              BlogGen AI
            </span>
          </div>
          <div className="flex items-center gap-3 sm:gap-4">
            <button
              className="text-neutral-text-secondary hover:text-neutral-text-primary transition-all duration-fast hover:scale-110 active:scale-95 p-2 -mr-2"
              aria-label="Settings"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header

