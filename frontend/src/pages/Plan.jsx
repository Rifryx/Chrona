import { useState } from "react"
import Calendar from '../components/Calendar.jsx'


const workingHours = {
  start: 8,
  end: 21,
}
const PX_PER_HOUR = 60
const PX_PER_MIN = PX_PER_HOUR / 60

const initialEvents = [
  { id: 1, title: 'Math Analysis', icon: '📘', start: '09:00', end: '11:00', color: '#3B82F6' },
  { id: 2, title: 'Linear Design Review', icon: '🎯', start: '11:00', end: '12:00', color: '#8B8B8B' },
  { id: 3, title: 'React Learning', icon: '💻', start: '13:00', end: '15:00', color: '#3B82F6' },
  { id: 4, title: 'Project Report', icon: '📄', start: '15:00', end: '16:00', color: '#8B8B8B' },
  { id: 5, title: 'Gym Session', icon: '🏋️', start: '18:00', end: '19:30', color: '#10B981' },
  { id: 6, title: 'Deep Work Read', icon: '📖', start: '20:00', end: '21:00', color: '#F97316' },
]

function parseTime(timeStr) {
  const parts = timeStr.split(":");
  const hours = Number(parts[0]);
  const minute = Number(parts[1]);

  return hours * 60 + minute
}

function getEventStyle(event) {
  const startMinutes = parseTime(event.start)
  const endMinites = parseTime(event.end)
  const gridStartMinutes = workingHours.start * 60

  const top = (startMinutes - gridStartMinutes) * PX_PER_MIN
  const height = ((endMinites - startMinutes) * PX_PER_MIN) -1

  return { top: `${top}px`, height: `${height}px`}

}

console.log(parseTime("09:30"))
function Plan() {
  const [events] = useState(initialEvents)
  const hours = Array.from({ length: workingHours.end - workingHours.start + 1}, (_, i) => workingHours.start + i);
  const [selectedDate, setSelectedDate] = useState(new Date())

  return (
    <div className="wrap ">
      <Calendar selectedDate={selectedDate} onSelectDate={setSelectedDate} />
      <div className="timeline-wrapper">
        <div className="timeline">
          {hours.map(hour => (
            <div key={hour} className="hour-row">
              <div className="hour-label">{String(hour).padStart(2, '0')}:00</div>
              <div className="hour-line"></div>
            </div>
          ))}
        </div>
        <div className="events-layer">
          {events.map(event => (
            <div key={event.id}
            className="event-block"
            style={{ ...getEventStyle(event), borderLeftColor: event.color}}
            >
              <div className="event-icon">{event.icon}</div>
              <div className="event-info">
                <div className="event-title">{event.title}</div>
                <div className="event-time">{event.start} - {event.end}</div>
              </div>
            </div>
            ))}
        </div>
      </div>
    </div>
  )
}

export default Plan