function TaskItem({ title, aiBadge, time, duration, color, iconBg, icon, priorityColor, done, onToggle }) {
  return (
    <div className="task-item" style={{ '--task-color': color }}>
      <div className="task-icon" style={{ background: iconBg }}>
        {icon}
      </div>

      <div className="task-info">
        <div className={`task-title ${done ? 'done' : ''}`}>
          {title} {aiBadge && <span className="ai-badge">AI</span>}
        </div>
        <div className="task-time">
          {time} <span className="dot-sep">•</span> {duration}
        </div>
      </div>

      <div className="task-right">
        <div className="priority-dot" style={{ background: priorityColor }} />
        <div className={`task-check ${done ? 'checked' : ''}`} onClick={onToggle}>
          <svg viewBox="0 0 24 24" fill="none">
            <path d="M5 13L9 17L19 7" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </div>
    </div>
  )
}

export default TaskItem
