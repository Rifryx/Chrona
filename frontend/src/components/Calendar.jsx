import { useState } from "react";

function getWeekDays(baseDate) {
    const dayOfWeek = baseDate.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

    const monday = new Date(baseDate);
    monday.setDate(baseDate.getDate() - diffToMonday);

    return Array.from({ length: 7 }, (_, i) => {
        const day = new Date(monday);
        day.setDate(monday.getDate() + i);
        return day;
    });
}

const dayLabels = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
const monthLabels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

const isSameDay = (dayA, dayB) =>
    dayA.getFullYear() === dayB.getFullYear() &&
    dayA.getMonth() === dayB.getMonth() &&
    dayA.getDate() === dayB.getDate();

function Calendar({ selectedDate, onSelectDate }) {
    const [baseDate, setBaseDate] = useState(new Date())

    const weekDays = getWeekDays(baseDate)

    function goToPrevWeek() {
        const prev = new Date(baseDate)
        prev.setDate(baseDate.getDate() - 7)
        setBaseDate(prev)
    }

    function goToNextWeek() {
        const next = new Date(baseDate)
        next.setDate(baseDate.getDate() + 7)
        setBaseDate(next)
    }

    return (
        <div className="block calendar">
            <div className="calendar-header">
                <div className="month-title">
                    {monthLabels[baseDate.getMonth()]} {baseDate.getFullYear()}
                </div>
                <div className="calendar-nav">
                    <button className="nav-arrow" onClick={goToPrevWeek}>
                        <svg viewBox="0 0 24 24" fill="none"><path d="M15 6L9 12L15 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>
                    </button>
                    <button className="nav-arrow" onClick={goToNextWeek}>
                        <svg viewBox="0 0 24 24" fill="none"><path d="M9 6L15 12L9 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>
                    </button>
                </div>
            </div>

            <div className="days-row">
                {weekDays.map(day => {
                    const active = isSameDay(day, selectedDate)
                    return (
                        <div
                            key={day.toISOString()}
                            className={`day-item ${active ? 'active' : ''}`}
                            onClick={() => onSelectDate(day)}
                        >
                            <div className="day-label">{dayLabels[day.getDay()]}</div>
                            <div className="day-num">{day.getDate()}</div>
                            {active && <div className="day-dot"></div>}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default Calendar