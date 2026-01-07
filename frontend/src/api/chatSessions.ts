import { api } from "./client";

export async function getSessions(){
    const response = await api.get("/sessions");
    return response.data;
}

export async function createSession(title = "New Chat") {
  const res = await api.post("/sessions", {title});
  return res.data;
}

export async function deleteSession(sessionId: number) {
  await api.delete(`/sessions/${sessionId}`);
}