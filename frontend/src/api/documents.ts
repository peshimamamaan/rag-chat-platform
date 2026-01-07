import { api } from "./client";

export async function uploadDocument(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await api.post("/documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
}

export async function embedDocument(documentId: number) {
  const res = await api.post(
    `/embeddings/document/${documentId}`
  );
  return res.data;
}