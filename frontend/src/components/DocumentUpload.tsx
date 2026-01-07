import { useState, useRef } from "react";
import {
  uploadDocument,
  embedDocument,
} from "../api/documents";

interface DocumentUploadProps {
  onUploaded: React.Dispatch<React.SetStateAction<number | null>>;
}

export default function DocumentUpload({ onUploaded }: DocumentUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState("");
  
  // Ref to trigger hidden file input
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async () => {
    if (!file) return;

    setStatus("Uploading document...");

    try {
      const doc = await uploadDocument(file);

      setStatus("Generating embeddings...");
      await embedDocument(doc.id);

      onUploaded(doc.id);
      
      setStatus("Document is RAG-ready!");
      
      // Optional: Clear success message after 3s to reset UI (or keep it to show success)
      setTimeout(() => {
        setFile(null);
        setStatus("");
      }, 3000);

    } catch (err) {
      console.error(err);
      setStatus("Upload failed");
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const selectedFile = e.target.files?.[0];
      if (selectedFile) {
          setFile(selectedFile);
          setStatus(""); // Clear any old status
      }
  };

  // --- RENDER LOGIC ---

  // 1. Success State (Green Check)
  if (status === "Document is RAG-ready!") {
    return (
       <div style={{ display: "flex", alignItems: "center", gap: 6, color: "#4ade80", fontSize: "0.85rem", fontWeight: 500 }}>
           <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
               <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
           </svg>
           <span>Ready</span>
       </div>
    );
  }

  // 2. Processing State (Loading)
  if (status.includes("Uploading") || status.includes("Generating") || status.includes("embeddings")) {
    return (
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <div style={{
                width: 12, height: 12, borderRadius: "50%", border: "2px solid #555", borderTopColor: "#3b82f6", animation: "spin 1s linear infinite"
            }}>
                <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
            </div>
            <span style={{ fontSize: "0.8rem", color: "#aaa" }}>{status}</span>
        </div>
    );
  }

  // 3. Default State (Idle or File Selected)
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
      {/* Hidden Native Input */}
      <input
        type="file"
        ref={fileInputRef}
        accept=".pdf,.txt"
        style={{ display: "none" }}
        onChange={handleFileChange}
      />

      {/* Button Logic: "Attach" vs "Upload" */}
      {!file ? (
        // State A: No file selected -> Show "Attach" button
        <button
          onClick={() => fileInputRef.current?.click()}
          style={{
            background: "#333",
            color: "#ccc",
            border: "1px solid #444",
            padding: "6px 12px",
            borderRadius: "6px",
            fontSize: "0.8rem",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: 6,
            transition: "all 0.2s"
          }}
          onMouseOver={(e) => e.currentTarget.style.background = "#404040"}
          onMouseOut={(e) => e.currentTarget.style.background = "#333"}
        >
          {/* Paperclip Icon */}
          <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
          </svg>
          Attach PDF
        </button>
      ) : (
        // State B: File Selected -> Show Name + Upload Button
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
            
            <span style={{ fontSize: "0.8rem", color: "#ececec", maxWidth: 120, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                {file.name}
            </span>

            <button 
                onClick={handleUpload}
                style={{
                    background: "#2563eb",
                    color: "#fff",
                    border: "none",
                    padding: "6px 12px",
                    borderRadius: "4px",
                    fontSize: "0.75rem",
                    fontWeight: 600,
                    cursor: "pointer"
                }}
            >
                Upload
            </button>
            
            {/* Cancel (X) Button */}
            <button 
                onClick={() => { setFile(null); setStatus(""); }}
                style={{ background: "none", border: "none", color: "#666", cursor: "pointer", display: "flex", alignItems: "center" }}
                title="Remove file"
            >
                <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
        </div>
      )}
      
      {/* Error Fallback */}
      {status === "Upload failed" && <span style={{ color: "#ef4444", fontSize: "0.8rem" }}>Failed</span>}
    </div>
  );
}