import { useState } from "react"

const initialTasks = [
  { id: 1, title: 'Math Analysis', ai: true, duration: '2h', date: 'Jul 29', category: 'Study', done: true },
  { id: 2, title: 'React Learning', ai: true, duration: '2h', date: 'Jul 29', category: 'Study', done: true },
  { id: 3, title: 'Project Report', ai: false, duration: '1h', date: 'Jul 30', category: 'Work', done: true },
  { id: 4, title: 'Linear Design Review', ai: true, duration: '1h', date: 'Jul 29', category: 'Work', done: false },
  { id: 5, title: 'Gym Session', ai: false, duration: '1.5h', date: 'Jul 29', category: 'Sport', done: false },
  { id: 6, title: 'Read — Deep Work', ai: false, duration: '1h', date: 'Jul 31', category: 'Personal', done: false },
]

const categoryMeta = {
  Study: { dot: 'var(--blue)', badgeColor: 'var(--blue)', badgeBg: 'rgba(59,130,246,0.15)' },
  Work: { dot: '#B0B0B0', badgeColor: 'var(--accent)', badgeBg: 'rgba(255,255,255,0.08)' },
  Sport: { dot: 'var(--emerald)', badgeColor: 'var(--emerald)', badgeBg: 'rgba(16,185,129,0.15)' },
  Personal: { dot: 'var(--orange)', badgeColor: 'var(--orange)', badgeBg: 'rgba(249,115,22,0.15)' },
}

const filters = ['All', 'Today', 'Study', 'Work', 'Sport', 'Personal']


 

function Tasks() {
  const [tasks, setTasks] = useState(initialTasks)
  const [activeFilter, setActiveFilter] = useState("All")

  function toggleTask(id) {
    setTasks(tasks.map(t => t.id === id ? { ...t, done: !t.done } : t))
  }

  const visibleTasks = activeFilter === "All" ? tasks : tasks.filter(t => t.category === activeFilter)

  const grouped = visibleTasks.reduce((acc, task) => {
    if (!acc[task.category]) acc[task.category] = []
    acc[task.category].push(task)
    return acc
  }, {})
  return (
    <div className="wrap tasks-page">
      <h1 className="page-title">My Tasks</h1>

      <div className="search-bar">
        <svg viewBox="0 0 24 24" fill="none">
          <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="1.8" />
          <path d="M21 21L16.5 16.5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
        </svg>
        <input type="text" placeholder="Search tasks..." />
      </div>

      <div className="filter-row">
        {filters.map(f => (
          <button
            key={f}
            className={`filter-pill ${activeFilter === f ? 'active' : ''}`}
            onClick={() => setActiveFilter(f)}
          >
            {f}
          </button>
        ))}
      </div>

      {Object.entries(grouped).map(([category, categoryTasks]) => (
        <div key={category} className="task-group">
          <div className="group-header">
            <span className="group-dot" style={{ background: categoryMeta[category].dot }}></span>
            <span className="group-name">{category.toUpperCase()}</span>
            <span className="group-count">{categoryTasks.length}</span>
          </div>

          {categoryTasks.map(task => (
            <div key={task.id} className="task-row">
              <div
                className={`task-checkbox ${task.done ? 'checked' : ''}`}
                onClick={() => toggleTask(task.id)}
              >
                <svg viewBox="0 0 24 24" fill="none">
                  <path d="M5 13L9 17L19 7" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>

              <div className="task-row-info">
                <div className={`task-row-title ${task.done ? 'done' : ''}`}>
                  {task.title} {task.ai && <span className="ai-badge">AI</span>}
                </div>
                <div className="task-row-meta">
                  <span>{task.duration}</span>
                  <span className="meta-sep">·</span>
                  <span>{task.date}</span>
                </div>
              </div>

              <span
                className="category-badge"
                style={{ color: categoryMeta[task.category].badgeColor, background: categoryMeta[task.category].badgeBg }}
              >
                {task.category}
              </span>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

export default Tasks
