import { api } from "./client";

export async function exportToDrive(payload:{
    content: string;
    format: "txt" | "docx" | "pdf";
    filename?: string;
    connection_id: string;
}) {
    const res = await api.post("/export/drive", payload);

    return res.data;
}