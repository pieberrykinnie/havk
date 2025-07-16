import { useState } from "react";
import { useRouter } from "next/router";
import { login } from "../../lib/api";
import { useAuth } from "../../lib/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const { setToken } = useAuth();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      setToken(data.access_token);
      router.push("/");
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <main className="flex flex-col items-center justify-center min-h-screen py-12">
      <h1 className="text-3xl font-bold mb-4">Login</h1>
      {error && <p className="text-red-500">{error}</p>}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 w-80">
        <input
          aria-label="Email address"
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border p-2"
          required
        />
        <input
          aria-label="Password"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2"
          required
        />
        <button type="submit" className="bg-green-600 text-white p-2 rounded">
          Log In
        </button>
      </form>
    </main>
  );
}