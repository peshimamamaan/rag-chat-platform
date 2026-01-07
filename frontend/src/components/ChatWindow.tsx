import { useEffect, useRef } from "react";
import type { ChatMessage } from "../types/chat";
import { exportToDrive } from "../api/export";

export default function ChatWindow({
  messages,
}: {
  messages: ChatMessage[];
}) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // const connectionId = localStorage.getItem("nango_connection_id");

  // const handleExport = async (
  //   content: string,
  //   format: "txt" | "docx" | "pdf"
  // ) => {
  //   if (!connectionId) {
  //     alert("Google Drive is not connected");
  //     return;
  //   }

  //   try {
  //     await exportToDrive({
  //       content,
  //       format,
  //       filename: `rag_answer.${format}`,
  //       connectionId,
  //     });

  //     alert(`Exported to Google Drive (${format.toUpperCase()})`);
  //   } catch (err) {
  //     console.error(err);
  //     alert("Failed to export");
  //   }
  // };

  return (
    <div
      style={{
        flex: 1,
        width: "100%",           // Ensure it takes full width
        boxSizing: "border-box",
        overflowY: "auto",
        padding: "20px",
        display: "flex",
        flexDirection: "column",
        gap: 12,
      }}
    >
      {/* Render Messages */}
      {messages.map((m) => {
        const isUser = m.role === "user";

        return (
          <div
            key={m.id}
            style={{
              display: "flex",
              width: "100%",
              justifyContent: isUser ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                maxWidth: "75%",
                padding: "12px 16px",
                borderRadius: 12,
                backgroundColor: isUser ? "#2f2f2f" : "#212121",
                color: "#fff",
                borderBottomRightRadius: isUser ? 2 : 12,
                borderBottomLeftRadius: isUser ? 12 : 2,
                wordBreak: "break-word"
              }}
            >
              <div style={{ fontSize: 11, opacity: 0.7, marginBottom: 6 }}>
                {m.role === "assistant" ? "AI Assistant" : "You"}
              </div>

              <div style={{ lineHeight: 1.5, whiteSpace: "pre-wrap" }}>
                {m.content}
              </div>

              {/* EXPORT BUTTONS (assistant only) */}
              {!isUser && (
                <div
                  style={{
                    marginTop: 10,
                    display: "flex",
                    gap: 8,
                  }}
                >
                </div>
              )}
            </div>
          </div>
        );
      })}

      {/* Invisible element to scroll to */}
      <div ref={bottomRef} />
    </div>
  );
}
