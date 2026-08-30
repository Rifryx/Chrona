import {useState } from "react"

const conversation = [
  {
    id: 1,
    role: 'user',
    text: 'Tomorrow at 3 PM solve math tests for 2 hours.',
  },
  {
    id: 2,
    role: 'assistant',
    comment: "I've scheduled this right after your lunch break when focus peaks. I also blocked 17:00–17:30 for review.",
    task: {
      title: 'Math test session',
      icon: '📘',
      iconColor: 'var(--blue)',
      day: 'Tomorrow',
      time: '18:00 - 20:00',
      category: 'Study',
      duration: '2 hours',
      tags: [
        { emoji: '📐', label: 'Math' },
        { emoji: '🎓', label: 'Study' },
        { emoji: '⚡', label: 'High' },
      ],
    },
  },
  {
    id: 3,
    role: 'user',
    text: 'Also remind me to call mom at 7 PM.',
  },
  {
    id: 4,
    role: 'assistant',
    comment: "Added a reminder task for tonight, right after dinner time.",
    task: {
      title: 'Call mom',
      icon: '📞',
      iconColor: 'var(--emerald)',
      day: 'Today',
      time: '19:00 - 19:15',
      category: 'Personal',
      duration: '15 min',
      tags: [
        { emoji: '📞', label: 'Call' },
        { emoji: '👪', label: 'Family' },
        { emoji: '🔔', label: 'Low' },
      ],
    },
  },
  
  // следующее сообщение — просто ещё один объект в этом же массиве
]

function Assistant() {


    return (
    <>
        <div className="substrate">
            <div className="wrap ">
                <h1 className="page-title">AI Assistant</h1>
            </div>
        </div>
        <div className="send-msg">
            <div className="wrap">
                <div className="substrate-msg">
                    <div className="input-field">
                        <input className="input-txt" type="text" placeholder="What do you need to do today?" />
                    </div>
                    <button className="send-btn">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M22 2L11 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" strokeWidth="2" strokeLinejoin="round"/>
                        </svg>
                    </button> 
                </div>
            </div>
        </div>
        <div className="wrap">
            <div className="chat">
                {conversation.map(msg =>{
                    if (msg.role === 'user') {
                        return (
                            <div key={msg.id} className="user-msg">
                                <p>{msg.text}</p>
                            </div>
                        )
                    }
                
                return (
                <div key={msg.id} className="chrona">
                    <div className="chona-dscr">
                        <div className="avatar companion"></div>
                        <h3 className="name">Chrona</h3>
                    </div>
                    <div className="crhona-msg">
                        <header className="task-bio">
                            <div className="icon-task" style={{background: `${msg.task.iconColor}22`}}>
                                <div className="emoji-task">{msg.task.icon}</div>
                            </div>
                            <div className="module-task">
                                <div className="dscr-task">
                                    <div className="name-task">{msg.task.title}</div>
                                    <div className="timeline-task">
                                        <h2 className="day-task">{msg.task.day}</h2>
                                        <p>•</p>
                                        <h2 className="time-task">{msg.task.time}</h2>
                                    </div>
                                </div>
                                <div className="circle-active"></div>
                            </div>
                    
                        </header>
                        <div className="about-task">
                            <div className="category-task">
                                <p className="task-title">CATEGORY</p>
                                <p className="category">{msg.task.category}</p>
                            </div>
                            <div className="category-task">
                                <p className="task-title">DURATION</p>
                                <p className="duration-task">{msg.task.duration}</p>
                            </div>
                        </div>
                        <div className="details-task">
                            {msg.task.tags.map((tag, i) => (
                                <div key={i} className="detail-substrate">
                                    <p>{tag.emoji} {tag.label}</p>
                                </div>
                            ))}
                        </div>
                        <p className="line"></p>
                        <div className="task-control">
                            <h3 className="task-report">{msg.comment}</h3>
                            <div className="final-task-btn">
                                <button className="add-to-schedule">Add To schedule</button>
                                <button className="edit-task">Edit</button>
                            </div>
                        </div>
                    </div>
                </div> 
                        )
                    })}
                   
            </div>
        </div>
    </>
    )
}

export default Assistant