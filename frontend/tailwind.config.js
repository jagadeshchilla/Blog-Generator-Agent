/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#6366F1',
          dark: '#4F46E5',
          light: '#818CF8',
        },
        neutral: {
          bg: '#FFFFFF',
          surface: '#F9FAFB',
          border: '#E5E7EB',
          text: {
            primary: '#111827',
            secondary: '#6B7280',
            muted: '#9CA3AF',
          },
        },
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
        info: '#3B82F6',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
        mono: ['Courier New', 'monospace'],
      },
      fontSize: {
        'hero': ['48px', { lineHeight: '1.2', fontWeight: '700' }],
        'section': ['36px', { lineHeight: '1.3', fontWeight: '600' }],
        'card-title': ['24px', { lineHeight: '1.4', fontWeight: '600' }],
      },
      borderRadius: {
        'sm': '4px',
        'md': '8px',
        'lg': '12px',
        'xl': '16px',
      },
      boxShadow: {
        'small': '0 1px 2px rgba(0,0,0,0.05)',
        'medium': '0 4px 6px -1px rgba(0,0,0,0.1)',
        'large': '0 10px 25px -5px rgba(0,0,0,0.1)',
        'xl': '0 20px 50px -10px rgba(0,0,0,0.15)',
      },
      transitionDuration: {
        'fast': '150ms',
        'normal': '300ms',
        'slow': '500ms',
      },
      screens: {
        'xs': '475px',
      },
    },
  },
  plugins: [],
}

