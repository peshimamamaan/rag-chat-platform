import type { ChatMessage } from "../types/chat";

export function buildChatText(messages: ChatMessage[]) {
  return messages
    .map((m) => {
      const role = m.role === "user" ? "User" : "Assistant";
      return `${role}:\n${m.content}\n`;
    })
    .join("\n----------------------\n\n");
}
