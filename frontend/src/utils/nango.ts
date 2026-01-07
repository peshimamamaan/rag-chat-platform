import Nango from "@nangohq/frontend";
import { getConnectSessionToken } from "../api/nango";

export async function connectGoogleDrive(): Promise<string> {
  try {
    const token = await getConnectSessionToken();

    const nango = new Nango({
      connectSessionToken: token,
    });

    console.log("Starting Nango auth…");

    const result = await nango.auth("google-drive");

    console.log("Nango auth result:", result);

    if (!result?.connectionId) {
      throw new Error("No connectionId returned");
    }

    localStorage.setItem("nango_connection_id", result.connectionId);
    return result.connectionId;
  } catch (err) {
    console.error("NANGO AUTH FAILED:", err);
    throw err; // IMPORTANT
  }
}
