import { connectGoogleDrive } from "./nango";

export async function getConnectionId(): Promise<string> {
  let connectionId = localStorage.getItem("nango_connection_id");

  if (!connectionId) {
    connectionId = await connectGoogleDrive();
  }

  return connectionId;
}
