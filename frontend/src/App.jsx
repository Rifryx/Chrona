import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Home from './pages/Home.jsx'
import Tasks from './pages/Tasks.jsx'
import Plan from './pages/Plan.jsx'
import Profile from './pages/Profile.jsx'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/tasks" element={<Tasks />} />
        <Route path="/plan" element={<Plan />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
      <Navbar />
    </BrowserRouter>
  )
}

export default App
