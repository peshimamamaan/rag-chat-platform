import { api } from "./client";

export async function listDriveFiles(connection_id: string) {
    const res = await api.get("/drive/files", {
        params: { connection_id }
    });
    return res.data.files;
}

export async function importDriveFiles(payload: {file_id: string, file_name: string, connection_id: string}) {
    const res = await api.post("/drive/import", payload);
    return res.data;
}