import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>HAVK Scarcity Solution</title>
      </Head>
      <main className="flex min-h-screen flex-col items-center justify-center py-12">
        <h1 className="text-4xl font-bold">HAVK – Hacking the Desert</h1>
        <p className="mt-4 text-lg text-center max-w-xl">
          Welcome to our project tackling global scarcity through innovative software.
        </p>
      </main>
    </>
  );
}