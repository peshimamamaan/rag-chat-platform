import { api } from "./client";

export async function askRag(question: string, document_id: number) {
    const response = await api.post("/rag/ask", { question, document_id });
    return response.data;
}