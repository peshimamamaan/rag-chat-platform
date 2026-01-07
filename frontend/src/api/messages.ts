import { api } from "./client";

export async function getMessages(sessionId: number) {
  const res = await api.get(`/messages/${sessionId}`);
  return res.data;
}

export async function sendMessage(
  sessionId: number,
  message: string
) {
  const res = await api.post("/chat", {
    session_id: sessionId,
    message
  });
  return res.data;
}

export async function sendRagMessage(message: string) {
  const res = await api.post("/rag", {
    question: message
  });
  return res.data;
}
