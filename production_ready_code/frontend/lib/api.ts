const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function register(email: string, password: string) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Registration failed");
  return res.json();
}

export async function login(email: string, password: string) {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);
  const res = await fetch(`${API_BASE}/auth/token`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error("Login failed");
  return res.json();
}

// Helper to include auth header
function authHeaders(token: string | null) {
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function listResources(token: string | null) {
  const res = await fetch(`${API_BASE}/resources/`, {
    headers: authHeaders(token),
  });
  if (!res.ok) throw new Error("Failed to fetch resources");
  return res.json();
}

export async function createResource(token: string | null, data: { name: string; description?: string; category?: string }) {
  const res = await fetch(`${API_BASE}/resources/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders(token) },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create resource");
  return res.json();
}

export async function listSolutions(token: string | null) {
  const res = await fetch(`${API_BASE}/solutions/`, {
    headers: authHeaders(token),
  });
  if (!res.ok) throw new Error("Failed to fetch solutions");
  return res.json();
}

export async function createSolution(token: string | null, data: { title: string; description?: string; resource_id: number }) {
  const res = await fetch(`${API_BASE}/solutions/`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders(token) },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create solution");
  return res.json();
}