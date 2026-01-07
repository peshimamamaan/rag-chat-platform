import { useState } from "react";

export default function ChatInput({
  onSend,
}: {
  onSend: (text: string) => void;
}) {
  const [text, setText] = useState("");

  const send = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div style={{ padding: 16, borderTop: "1px solid #ddd", display: "flex", gap: 8, alignItems: "center" }}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ flex: 1, padding: 8 }}
        onKeyDown={(e) => { if (e.key === "Enter") send(); }}
      />
      <button onClick={send}>Send</button>
    </div>
  );
}
