import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/App.css'
import App from './App.jsx'
import { FournisseurTheme } from './contexts/ContexteTheme'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <FournisseurTheme>
      <App />
    </FournisseurTheme>
  </StrictMode>,
)