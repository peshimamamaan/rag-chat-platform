export async function getConnectSessionToken(): Promise<string> {
  const res = await fetch("/api/nango/session", {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("Failed to get Nango connect session");
  }

  const json = await res.json();

   const token = json?.data?.token;
   console.log(token);
   

   if (!token) {
    console.error("Invalid Nango session response:", json);
    throw new Error("Nango connect session token missing");
  }

  return json.data.token;
}
