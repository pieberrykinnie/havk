import type { AppProps } from "next/app";
import "../styles/globals.css";
import { AuthProvider } from "../lib/AuthContext";
import NavBar from "../components/NavBar";

export default function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <NavBar />
      <Component {...pageProps} />
    </AuthProvider>
  );
}