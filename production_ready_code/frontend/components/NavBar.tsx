import Link from "next/link";
import { useAuth } from "../lib/AuthContext";

export default function NavBar() {
  const { token, logout } = useAuth();
  return (
    <nav className="w-full bg-gray-900 text-white p-4 flex justify-between">
      <div className="flex gap-4 items-center">
        <Link className="font-bold" href="/">
          HAVK
        </Link>
        {token && (
          <>
            <Link href="/resources">Resources</Link>
            <Link href="/solutions">Solutions</Link>
          </>
        )}
      </div>
      <div>
        {token ? (
          <button onClick={logout} className="text-sm hover:underline">
            Logout
          </button>
        ) : (
          <Link href="/auth/login" className="text-sm hover:underline">
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}