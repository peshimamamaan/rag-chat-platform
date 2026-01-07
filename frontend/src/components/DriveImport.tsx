// src/components/DriveImport.tsx
import { useState, useRef, useEffect } from "react";
import { listDriveFiles, importDriveFiles } from "../api/drive";

export default function DriveImport({
  onImported,
}: {
  onImported: (docId: number) => void;
}) {
  const [files, setFiles] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const connectionId =
    localStorage.getItem("nango_connection_id") ||
    "d78542b4-349e-4ab2-933d-2356391fbabd";

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleToggleOpen = async () => {
    const nextState = !isOpen;
    setIsOpen(nextState);
    if (nextState && files.length === 0) {
      loadFiles();
    }
  };

  const loadFiles = async () => {
    setLoading(true);
    try {
      const data = await listDriveFiles(connectionId);
      setFiles(data);
    } catch (err) {
      console.error("Drive list error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async (fileId: string, connectionId: string) => {
    setLoading(true);
    try {
      const file = files.find(f => f.id === fileId);
        if (!file) {
        alert("File not found");
        return;
      }
      const doc = await importDriveFiles({file_id: fileId, connection_id: connectionId, file_name: files.find(f => f.id === fileId)?.name});
      console.log(fileId, connectionId, files.find(f => f.id === fileId)?.name);
      
      onImported(doc.id);
      setIsOpen(false); // Close after success
    } catch (err) {
      alert("Import failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ position: "relative" }} ref={dropdownRef}>
      {/* TRIGGER BUTTON (Matches Attach PDF style) */}
      <button
        onClick={handleToggleOpen}
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
          transition: "all 0.2s",
        }}
        onMouseOver={(e) => (e.currentTarget.style.background = "#404040")}
        onMouseOut={(e) => (e.currentTarget.style.background = "#333")}
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 19l-9.108-15.022c-.412-.679-1.372-.679-1.784 0L2 19h20z" />
          <path d="M16.142 19L12 12.155 7.857 19h8.285z" />
        </svg>
        Drive Import
      </button>

      {/* DROPDOWN MENU */}
      {isOpen && (
        <div
          style={{
            position: "absolute",
            top: "calc(100% + 8px)",
            left: 0,
            width: "280px",
            maxHeight: "350px",
            backgroundColor: "#212121",
            border: "1px solid #444",
            borderRadius: "8px",
            boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)",
            zIndex: 100,
            overflow: "hidden",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <div style={{ padding: "10px 12px", borderBottom: "1px solid #333", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span style={{ fontSize: "0.75rem", fontWeight: 600, color: "#9ca3af", textTransform: "uppercase" }}>Google Drive Files</span>
            {loading && <div style={{ width: 12, height: 12, borderRadius: "50%", border: "2px solid #555", borderTopColor: "#3b82f6", animation: "spin 1s linear infinite" }} />}
          </div>

          <div style={{ overflowY: "auto", padding: "4px 0" }}>
            {files.length === 0 && !loading ? (
              <div style={{ padding: "20px", textAlign: "center", color: "#666", fontSize: "0.8rem" }}>No files found</div>
            ) : (
              files.map((f) => (
                <div
                  key={f.id}
                  onClick={() => handleImport(f.id, connectionId)}
                  style={{
                    padding: "10px 12px",
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    gap: 10,
                    transition: "background 0.2s",
                  }}
                  onMouseOver={(e) => (e.currentTarget.style.background = "#2a2a2a")}
                  onMouseOut={(e) => (e.currentTarget.style.background = "transparent")}
                >
                  <span
                    style={{
                      fontSize: "0.85rem",
                      color: "#ececec",
                      whiteSpace: "nowrap",
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      flex: 1,
                    }}
                  >
                    {f.name}
                  </span>
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" strokeWidth="2">
                    <path d="M7 16l-4-4m0 0l4-4m-4 4h18" />
                  </svg>
                </div>
              ))
            )}
          </div>
          <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
        </div>
      )}
    </div>
  );
}