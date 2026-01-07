import { useEffect, useState } from "react";
import { getSessions, createSession } from "../api/chatSessions";
import { getMessages, sendMessage } from "../api/messages";
import SessionList from "../components/SessionList";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";
import DocumentUpload from "../components/DocumentUpload";
import DriveImport from "../components/DriveImport";
import { askRag } from "../api/rag";
import type { ChatSession, ChatMessage } from "../types/chat";

import { buildChatText } from "../utils/exportChat";
import { exportToDrive } from "../api/export";
import { deleteSession } from "../api/chatSessions";
import { connectGoogleDrive } from "../utils/nango";
// import { getConnectionId } from "../utils/getConnectionId";

export default function ChatPage() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSession, setActiveSession] = useState<number | null>(null);
  const [activeDocumentId, setActiveDocumentId] = useState<number | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [useDocuments, setUseDocuments] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [exportFormat, setExportFormat] = useState<"txt" | "pdf" | "docx">("txt");


  useEffect(() => {
    getSessions().then(setSessions);
  }, []);

  const exportChat = async (exportFormat: "txt" | "pdf" | "docx") => {
    if (!activeSession || messages.length === 0) return;

    setIsExporting(true);
    try {
      let connectionId = localStorage.getItem("nango_connection_id");

      if (!connectionId) {
        connectionId = await connectGoogleDrive();
      }
      const chatText = buildChatText(messages);
      // const connectionId = localStorage.getItem("nango_connection_id");
      console.log("Export clicked")
      // const connectionId = await getConnectionId();
      await exportToDrive({
        content: chatText,
        format: exportFormat,
        filename: `chat_session_${activeSession}.${exportFormat}`,
        connection_id: connectionId,
      });
      alert("Chat exported to Google Drive");
    } catch (error) {
      console.error("EXPORT ERROR:", error);
      alert("Failed to export chat");
    } finally {
      setIsExporting(false);
    }
  };


  const loadMessages = async (id: number) => {
    setActiveSession(id);
    const msgs = await getMessages(id);
    setMessages(msgs);
  };

  const newSession = async () => {
    const session = await createSession();
    setSessions([session, ...sessions]);
    loadMessages(session.id);
  };

  const handleDeleteSession = async (id: number) => {
    if (!window.confirm("Delete this chat session?")) return;

    await deleteSession(id);

    setSessions((prev) => prev.filter((s) => s.id !== id));

    if (activeSession === id) {
      setActiveSession(null);
      setMessages([]);
    }
  };

  const send = async (text: string) => {
    if (!activeSession) return;

    const userMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content: text,
    };

    setMessages((prev) => [...prev, userMessage]);

    if (useDocuments) {
      if (activeDocumentId === null) {
        setMessages((prev) => [
          ...prev,
          {
            id: Date.now() + 1,
            role: "assistant",
            content: "Please upload a document first.",
          },
        ]);
        return;
      }

      const res = await askRag(text, activeDocumentId, activeSession);
      const assistantMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: res.answer,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } else {
      const res = await sendMessage(activeSession, text);
      setMessages((prev) => [...prev, res.assistant]);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", width: "100vw", backgroundColor: "#1a1a1a", color: "#ececec", overflow: "hidden" }}>
      
      {/* SIDEBAR */}
      <SessionList
        sessions={sessions}
        activeId={activeSession}
        onSelect={loadMessages}
        onNew={newSession}
        onDelete={handleDeleteSession}
      />

      {/* RIGHT COLUMN */}
      <div style={{ 
        flex: 1, 
        display: "flex", 
        flexDirection: "column", 
        height: "100vh", 
        overflow: "hidden" ,
        minWidth: 0
      }}>
        
        {/* HEADER: Context & Actions Toolbar */}
        <div style={{ 
          height: "70px", // Fixed height for consistency
          padding: "0 24px", 
          borderBottom: "1px solid #333",
          backgroundColor: "#212121",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)" // Subtle shadow for depth
        }}>
          
          {/* LEFT: Context Controls (Grouped horizontally) */}
          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            
            {/* Label */}
            <span style={{ 
              fontSize: "0.75rem", 
              textTransform: "uppercase", 
              letterSpacing: "0.05em", 
              color: "#6b7280", 
              fontWeight: 600 
            }}>
              Context
            </span>

            {/* Vertical Divider */}
            <div style={{ width: "1px", height: "24px", backgroundColor: "#404040" }}></div>

            {/* Controls Group */}
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <DocumentUpload onUploaded={setActiveDocumentId}/>
              
              <DriveImport onImported={setActiveDocumentId} />

              <label style={{ 
                display: "flex", 
                alignItems: "center", 
                gap: 8, 
                cursor: "pointer", 
                fontSize: "0.9rem", 
                color: useDocuments ? "#fff" : "#9ca3af", // White if active, gray if inactive
                transition: "color 0.2s",
                userSelect: "none"
              }}>
                <input
                  type="checkbox"
                  checked={useDocuments}
                  onChange={(e) => setUseDocuments(e.target.checked)}
                  style={{ 
                    accentColor: "#3b82f6", 
                    width: "16px", 
                    height: "16px",
                    cursor: "pointer"
                  }}
                />
                <span>Ask with RAG</span>
              </label>
            </div>
          </div>

          {/* RIGHT: Actions (Export) */}
          {/* <div>
            <button
              onClick={exportChat}
              disabled={messages.length === 0 || isExporting}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                padding: "8px 16px",
                background: messages.length === 0 ? "transparent" : "#2563eb", 
                color: messages.length === 0 ? "#525252" : "#fff",
                borderRadius: "6px",
                border: "1px solid",
                borderColor: messages.length === 0 ? "#404040" : "#2563eb",
                cursor: messages.length === 0 || isExporting ? "not-allowed" : "pointer",
                fontSize: "0.85rem",
                fontWeight: 500,
                transition: "all 0.2s ease"
              }}
            >
              {isExporting ? "Saving..." : "Export Chat"}
              {!isExporting && (
                 <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                 </svg>
              )}
            </button>
          </div> */}
          <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
            {/* FORMAT SELECTOR */}
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <label style={{ fontSize: "0.85rem", color: "#6b7280", fontWeight: 500 }}>
                Format
              </label>
              <select
                value={exportFormat}
                onChange={(e) => setExportFormat(e.target.value as any)}
                style={{
                  background: "#1a1a1a",
                  color: "#fff",
                  border: "1px solid #444",
                  padding: "6px 10px",
                  borderRadius: 6,
                  fontSize: "0.85rem",
                  outline: "none",
                  cursor: "pointer"
                }}
              >
                <option value="txt">TXT</option>
                <option value="pdf">PDF</option>
                <option value="docx">DOCX</option>
              </select>
            </div>

            <button
              onClick={() => exportChat(exportFormat)} // Pass format to your function
              disabled={messages.length === 0 || isExporting}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                padding: "8px 16px",
                background: messages.length === 0 ? "transparent" : "#2563eb", 
                color: messages.length === 0 ? "#525252" : "#fff",
                borderRadius: "6px",
                border: "1px solid",
                borderColor: messages.length === 0 ? "#404040" : "#2563eb",
                cursor: messages.length === 0 || isExporting ? "not-allowed" : "pointer",
                fontSize: "0.85rem",
                fontWeight: 600,
                transition: "all 0.2s ease"
              }}
            >
              {isExporting ? "Saving..." : "Export Chat"}
              {!isExporting && (
                <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
              )}
            </button>
          </div>
        
        </div>
  

        {/* MIDDLE: Chat Window */}
        <ChatWindow messages={messages} />

        {/* FOOTER: Input */}
        <div style={{ borderTop: "1px solid #333", backgroundColor: "#212121" }}>
           <ChatInput onSend={send} />
        </div>

      </div>
    </div>
  );

}