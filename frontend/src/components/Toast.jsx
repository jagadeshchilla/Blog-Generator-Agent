import { CheckCircle, XCircle, X } from 'lucide-react'
import { useEffect } from 'react'

const Toast = ({ message, type = 'success' }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      // Toast will be removed by parent component
    }, 3000)
    return () => clearTimeout(timer)
  }, [])

  const Icon = type === 'success' ? CheckCircle : XCircle
  const bgColor = type === 'success' ? 'bg-success' : 'bg-error'

  return (
    <div
      className={`fixed top-20 sm:top-24 right-2 sm:right-4 left-2 sm:left-auto ${bgColor} text-white px-4 sm:px-6 py-3 sm:py-4 rounded-lg shadow-xl flex items-center gap-3 animate-bounce-in z-50 max-w-md mx-auto sm:mx-0 transform-gpu`}
      role="alert"
    >
      <Icon className="w-5 h-5 flex-shrink-0 animate-scale-in" />
      <p className="flex-1 text-sm sm:text-base font-medium">{message}</p>
    </div>
  )
}

export default Toast

