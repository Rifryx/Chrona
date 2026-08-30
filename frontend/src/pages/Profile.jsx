import { useState } from "react"

function generateActivityDay(days = 91) {
  const today = new Date()
  const targetDay = new Date(today)
  targetDay.setDate(today.getDate() - days)

  const dayOffWeek = targetDay.getDay()
  const diffToMonday = dayOffWeek === 0 ? 6 : dayOffWeek - 1

  const startMonday = new Date(targetDay)
  startMonday.setDate(targetDay.getDate() - diffToMonday)

  const data = []
  const currentDate = new Date(startMonday)

  while (currentDate <= today) {
    data.push({
      date: new Date(currentDate),
      level: Math.floor(Math.random() * 5),
    })
    currentDate.setDate(currentDate.getDate() + 1)
  }

  return data
}

const activityData = generateActivityDay(91)
const taskOnWeek = 38

const categories = [
  { name: "Study", count: 18, percent: 42, color: "#3B82F6" },
  { name: "Work", count: 13, percent: 30, color: "#9ca3af" },
  { name: "Sport", count: 7, percent: 16, color: "#10B981" },
  { name: "Personal", count: 5, percent: 12, color: "#F97316" },
]

const achievements = [
  {
    icon: "🔥",
    title: "7-Day Streak",
    desc: "Complete tasks 7 days in a row",
    earned: true,
    iconBg: "rgba(249, 115, 22, 0.15)",
    iconColor: "#F97316",
  },
  {
    icon: "⚡",
    title: "Productivity Pro",
    desc: "90%+ score for 5 days",
    earned: true,
    iconBg: "rgba(167, 139, 250, 0.15)",
    iconColor: "#A78BFA",
  },
]

const weekDays = ["M", "T", "W", "T", "F", "S", "S"]

function Profile() {
  return (
    <div className="wrap" style={{ paddingTop: 24 }}>
      <div className="profile-header">
        <div className="profile-info">
          <div className="profile-avatar">A</div>
          <div className="profile-text">
            <div className="profile-name">Alexander Chen</div>
            <div className="profile-handle">
              @alexanderchen <span className="profile-premium">· Premium</span>
            </div>
          </div>
        </div>
        <button className="edit-btn">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="14" height="14">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
          </svg>
          Edit
        </button>
      </div>

  

      {/* ─── Stats ─── */}
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-icon" style={{ color: "#F97316" }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" width="24" height="24">
              <path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z" />
            </svg>
          </div>
          <div className="stat-value" style={{ color: "#F97316" }}>14</div>
          <div className="stat-label">Days</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ color: "#10B981" }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" width="24" height="24">
              <path d="M20 6L9 17l-5-5" />
            </svg>
          </div>
          <div className="stat-value" style={{ color: "#10B981" }}>247</div>
          <div className="stat-label">Tasks</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon" style={{ color: "#F97316" }}>
            <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <div className="stat-value" style={{ color: "#F97316" }}>94</div>
          <div className="stat-label">%</div>
        </div>
      </div>

      {/* ─── Weekly Activity ─── */}
      <div className="block activity">
        <div className="dscr-activity">
          <span>Weekly Activity</span>
          <span>{taskOnWeek} tasks this week</span>
        </div>

        <div className="heatmap-container">
          <div className="heatmap-labels">
            {weekDays.map((d, i) => (
              <span key={i}>{d}</span>
            ))}
          </div>
          <div className="activity-heatmap">
            {activityData.map((day, i) => (
              <div
                key={i}
                className={`heatmap-cell level-${day.level}`}
                title={day.date.toLocaleDateString()}
              />
            ))}
          </div>
        </div>

        <div className="info-activity">
          <span>Less</span>
          <div className="heatmap-cell level-0" />
          <div className="heatmap-cell level-1" />
          <div className="heatmap-cell level-2" />
          <div className="heatmap-cell level-3" />
          <div className="heatmap-cell level-4" />
          <span>More</span>
        </div>
      </div>

      {/* ─── Category Breakdown ─── */}
      <div className="block categories">
        <div className="categories-header">Category Breakdown</div>
        <div className="category-list">
          {categories.map((cat) => (
            <div className="category-row" key={cat.name}>
              <div
                className="category-dot"
                style={{ backgroundColor: cat.color }}
              />
              <div className="category-name">{cat.name}</div>
              <div className="category-track">
                <div
                  className="category-progress"
                  style={{
                    width: `${cat.percent}%`,
                    backgroundColor: cat.color,
                  }}
                />
              </div>
              <div className="category-meta">
                <span className="category-count">{cat.count} tasks</span>
                <span className="category-percent">{cat.percent}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ─── Achievements ─── */}
      <div className="block achievements">
        <div className="achievements-header">Achievements</div>
        <div className="achievements-grid">
          {achievements.map((ach) => (
            <div className="achievement-card" key={ach.title}>
              <div
                className="achievement-icon"
                style={{
                  background: ach.iconBg,
                  color: ach.iconColor,
                }}
              >
                {ach.icon}
              </div>
              <div className="achievement-title">{ach.title}</div>
              <div className="achievement-desc">{ach.desc}</div>
              {ach.earned && (
                <div className="achievement-earned">
                  EARNED
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="3"
                    width="14"
                    height="14"
                    style={{ color: "#10B981" }}
                  >
                    <path d="M20 6L9 17l-5-5" />
                  </svg>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Profile