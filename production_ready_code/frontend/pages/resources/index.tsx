import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { useAuth } from "../../lib/AuthContext";
import { listResources, createResource } from "../../lib/api";

interface Resource {
  id: number;
  name: string;
  description?: string;
  category?: string;
}

export default function ResourcesPage() {
  const { token } = useAuth();
  const router = useRouter();
  const [resources, setResources] = useState<Resource[]>([]);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) {
      router.push("/auth/login");
    } else {
      load();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  async function load() {
    try {
      const data = await listResources(token);
      setResources(data);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    try {
      await createResource(token, { name, description, category });
      setName("");
      setDescription("");
      setCategory("");
      load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Resources</h1>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <form onSubmit={handleCreate} className="flex gap-2 mb-4 flex-wrap">
        <input
          className="border p-2 flex-1"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          className="border p-2 flex-1"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <input
          className="border p-2 flex-1"
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
          Add
        </button>
      </form>
      <ul className="space-y-2">
        {resources.map((r) => (
          <li key={r.id} className="border p-3 rounded shadow-sm">
            <h3 className="font-semibold">{r.name}</h3>
            {r.description && <p className="text-sm">{r.description}</p>}
            {r.category && <span className="text-xs bg-gray-200 px-2 py-1 rounded">{r.category}</span>}
          </li>
        ))}
      </ul>
    </main>
  );
}