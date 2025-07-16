import { useState } from 'react';

export default function Home() {
  const [prompt, setPrompt] = useState('');
  const [animationUrl, setAnimationUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setAnimationUrl('');
    const res = await fetch('http://localhost:8000/animate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await res.json();
    setAnimationUrl(data.animation_url);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: 'auto', padding: 32 }}>
      <h1>HAVK AI Animation Demo</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="Describe your animation..."
          style={{ width: '80%', padding: 8 }}
        />
        <button type="submit" disabled={loading} style={{ marginLeft: 8 }}>
          {loading ? 'Generating...' : 'Animate'}
        </button>
      </form>
      {animationUrl && (
        <div style={{ marginTop: 24 }}>
          <h2>Result</h2>
          <video src={animationUrl} controls width="100%" />
        </div>
      )}
    </div>
  );
}