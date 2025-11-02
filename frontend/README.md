# BlogGen AI Frontend

A modern, responsive React frontend for the BlogGen AI application.

## Features

- 🎨 Modern UI/UX design following best practices
- 📱 Fully responsive (mobile, tablet, desktop)
- ⚡ Built with Vite for fast development
- 🎯 Two blog generation modes: Topic and YouTube
- 🌍 Multi-language support
- 📝 Markdown rendering for blog content
- 💾 Copy, download, and share functionality

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Configuration

The frontend connects to the backend API. By default, it expects the API at `http://localhost:8000`.

You can configure the API URL by creating a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── Header.jsx
│   │   ├── TabNavigation.jsx
│   │   ├── TopicBlogForm.jsx
│   │   ├── YouTubeBlogForm.jsx
│   │   ├── BlogPreview.jsx
│   │   └── Toast.jsx
│   ├── services/         # API services
│   │   └── api.js
│   ├── App.jsx           # Main app component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **React Markdown** - Markdown rendering
- **Axios** - HTTP client
- **Lucide React** - Icons

## Design System

The design follows the specifications in `DESIGN_DOCUMENT.md`:
- Color palette with Indigo primary color
- Inter font family
- Consistent spacing and shadows
- Smooth animations and transitions

