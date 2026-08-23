import { useState } from 'react'
import TaskItem from '../components/TaskItem.jsx'
import Calendar from '../components/Calendar.jsx'

const initialTasks = [
  { id: 1, title: 'Math Analysis', aiBadge: true, time: '09:00 — 11:00', duration: '2h', color: 'var(--blue)', iconBg: 'rgba(59,130,246,0.15)', priorityColor: '#EF4444', done: true },
  { id: 2, title: 'React Learning', aiBadge: true, time: '13:00 — 15:00', duration: '2h', color: 'var(--blue)', iconBg: 'rgba(59,130,246,0.15)', priorityColor: '#EF4444', done: true },
  { id: 3, title: 'Project Report', aiBadge: false, time: '15:30 — 16:30', duration: '1h', color: '#fff', iconBg: 'rgba(255,255,255,0.1)', priorityColor: 'var(--orange)', done: true },
  { id: 4, title: 'Gym Session', aiBadge: false, time: '18:00 — 19:30', duration: '1.5h', color: 'var(--emerald)', iconBg: 'rgba(16,185,129,0.15)', priorityColor: 'var(--emerald)', done: false },
  { id: 5, title: 'Read — Deep Work', aiBadge: false, time: '20:00 — 21:00', duration: '1h', color: 'var(--orange)', iconBg: 'rgba(249,115,22,0.15)', priorityColor: 'var(--orange)', done: false },
  { id: 6, title: 'Linear Design Review', aiBadge: true, time: '11:30 — 12:30', duration: '1h', color: '#fff', iconBg: 'rgba(236,72,153,0.15)', priorityColor: '#EF4444', done: false },
]


const categories = [
  { label: 'STUDY', percent: 80, color: 'var(--blue)' },
  { label: 'WORK', percent: 45, color: '#fff' },
  { label: 'SPORT', percent: 0, color: 'var(--emerald)' },
  { label: 'PERSONAL', percent: 0, color: 'var(--orange)' },
]

function Home() {
  const [tasks, setTasks] = useState(initialTasks)
  const [selectedDate, setSelectedDate] = useState(new Date())

  function toggleTask(id) {
    setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t))
  }

  return (
    <>
      <header className="user">
        <div className="wrap">

          {/* Карточка приветствия */}
          <div className="block first">
            <div className="first-line">
              <section className="description">
                <div className="avatar"></div>
                <div className="bio">
                  <div className="greeting">Good morning</div>
                  <div className="us-name">Rifryx</div>
                </div>
              </section>
              <div className="mini-btn">
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M18 9C18 5.69 15.31 3 12 3C8.69 3 6 5.69 6 9V14L4 17H20L18 14V9Z"
                    stroke="currentColor" strokeWidth="1.4" strokeLinejoin="round" />
                  <path d="M10 20C10.5 20.63 11.19 21 12 21C12.81 21 13.5 20.63 14 20"
                    stroke="currentColor" strokeWidth="1.4" strokeLinecap="round" />
                </svg>
              </div>
            </div>
            <div className="second-line">
              <div className="main-btn">Перестроить день</div>
            </div>
          </div>

          <Calendar selectedDate={selectedDate} onSelectDate={setSelectedDate} />

          {/* Дневной прогресс */}
          <div className="block progress">
            <div className="progress-header">
              <div className="progress-label">DAILY PROGRESS</div>
              <div className="progress-count">3 of 6<span>tasks done</span></div>
            </div>
            <div className="progress-percent">50%</div>
            <div className="progress-categories">
              {categories.map(c => (
                <div key={c.label} className="category-item">
                  <div className="category-bar">
                    <div className="category-fill" style={{ width: `${c.percent}%`, background: c.color }}></div>
                  </div>
                  <div className="category-label">{c.label}</div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </header>

      {/* Today's Schedule */}
      <div className="wrap">      
        <div className="schedule-header">
          <div className="schedule-title">Today's Schedule</div>
          <a href="#" className="see-all">See all</a>
        </div>

        <div className="block schedule">
          <div className="task-list">
            {tasks.map(task => (
              <TaskItem
                key={task.id}
                {...task}
                icon={null}
                onToggle={() => toggleTask(task.id)}
              />
            ))}
          </div>
        </div>
      </div>
    </>
  )
}

export default Home
