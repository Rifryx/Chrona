import { NavLink } from 'react-router-dom'

function Navbar() {
  const linkClass = ({ isActive }) => `nav-item ${isActive ? 'active' : ''}`

  return (
    <nav className="navbar">
      <NavLink to="/" className={linkClass}>
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M3 10.5L12 3L21 10.5V20C21 20.55 20.55 21 20 21H4C3.45 21 3 20.55 3 20V10.5Z"
            stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
          <path d="M9 21V14H15V21" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round" />
        </svg>
        <span>Главная</span>
      </NavLink>

      <NavLink to="/tasks" className={linkClass}>
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M5 6H19" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M5 12H19" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M5 18H19" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          <circle cx="3" cy="6" r="0.8" fill="currentColor" />
          <circle cx="3" cy="12" r="0.8" fill="currentColor" />
          <circle cx="3" cy="18" r="0.8" fill="currentColor" />
        </svg>
        <span>Задачи</span>
      </NavLink>

      <button className="add-btn">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M12 5V19" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M5 12H19" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
      </button>

      <NavLink to="/plan" className={linkClass}>
        <svg viewBox="0 0 24 24" fill="none">
          <rect x="3.5" y="5" width="17" height="16" rx="2" stroke="currentColor" strokeWidth="1.8" />
          <path d="M7 3V7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M17 3V7" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
          <path d="M3.5 10H20.5" stroke="currentColor" strokeWidth="1.8" />
        </svg>
        <span>План</span>
      </NavLink>

      <NavLink to="/profile" className={linkClass}>
        <svg viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="8" r="3.5" stroke="currentColor" strokeWidth="1.8" />
          <path d="M5 21C5 17.7 8.13 15 12 15C15.87 15 19 17.7 19 21" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
        <span>Профиль</span>
      </NavLink>
    </nav>
  )
}

export default Navbar
