import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { useAuth } from "../../lib/AuthContext";
import { listResources, listSolutions, createSolution } from "../../lib/api";

interface Solution {
  id: number;
  title: string;
  description?: string;
  resource_id: number;
}
interface ResourceOption {
  id: number;
  name: string;
}

export default function SolutionsPage() {
  const { token } = useAuth();
  const router = useRouter();
  const [solutions, setSolutions] = useState<Solution[]>([]);
  const [resources, setResources] = useState<ResourceOption[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [resourceId, setResourceId] = useState<number | "">("");
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
      const [solData, resData] = await Promise.all([listSolutions(token), listResources(token)]);
      setSolutions(solData);
      setResources(resData);
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (resourceId === "") return;
    try {
      await createSolution(token, { title, description, resource_id: Number(resourceId) });
      setTitle("");
      setDescription("");
      setResourceId("");
      load();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <main className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Solutions</h1>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <form onSubmit={handleCreate} className="flex gap-2 mb-4 flex-wrap">
        <input
          aria-label="Solution title"
          className="border p-2 flex-1"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <input
          aria-label="Solution description"
          className="border p-2 flex-1"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <select
          aria-label="Related resource"
          className="border p-2 flex-1"
          value={resourceId}
          onChange={(e) => setResourceId(e.target.value === "" ? "" : Number(e.target.value))}
          required
        >
          <option value="">Select Resource</option>
          {resources.map((r) => (
            <option key={r.id} value={r.id}>
              {r.name}
            </option>
          ))}
        </select>
        <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded">
          Add
        </button>
      </form>
      <ul className="space-y-2">
        {solutions.map((s) => (
          <li key={s.id} className="border p-3 rounded shadow-sm">
            <h3 className="font-semibold">{s.title}</h3>
            {s.description && <p className="text-sm mb-1">{s.description}</p>}
            <span className="text-xs bg-blue-200 px-2 py-1 rounded">Resource #{s.resource_id}</span>
          </li>
        ))}
      </ul>
    </main>
  );
}