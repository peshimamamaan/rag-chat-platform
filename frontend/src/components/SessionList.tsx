import type { ChatSession } from "../types/chat";

interface Props {
  sessions: ChatSession[];
  activeId: number | null;
  onSelect: (id: number) => void;
  onNew: () => void;
  onDelete: (id: number) => void;
}

export default function SessionList({
  sessions,
  activeId,
  onSelect,
  onNew,
  onDelete
}: Props) {
  return (
    <div style={{ width: 250, borderRight: "1px solid #ddd", padding: 12 }}>
      <button onClick={onNew}>+ New Chat</button>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {sessions.map((s) => (
          <li
            key={s.id}
            onClick={() => onSelect(s.id)}
            // style={{
            //   cursor: "pointer",
            //   padding: 8,
            //   borderRadius: 6,
            //   background:
            //     activeId === s.id ? "#eee" : "transparent",
            //   color: activeId === s.id ? "#000" : "#fff",
            // }}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              padding: 8,
              marginBottom: 6,
              background: activeId === s.id ? "#2a2a2a" : "transparent",
              cursor: "pointer",
              borderRadius: 6,
            }}
          >
            Chat #{s.id}
          
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(s.id);
              }}
              style={{
                background: "transparent",
                border: "none",
                color: "#f87171",
                cursor: "pointer",
                fontSize: "0.8rem",
              }}
            >
              ✕
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
