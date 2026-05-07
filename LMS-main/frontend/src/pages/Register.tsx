import { type FormEvent, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAuth } from "../auth";

export default function Register() {
  const { user, register } = useAuth();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  if (user) return <Navigate to="/" replace />;

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setErr(null);
    setBusy(true);
    try {
      await register(email, password, name);
    } catch {
      setErr("Could not register. Email may already be in use.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4">
      <img
        src="/logo.png"
        alt=""
        className="mb-8 h-12 w-auto object-contain"
        onError={(e) => {
          if (e.currentTarget.src.endsWith("/logo.svg")) return;
          e.currentTarget.src = "/logo.svg";
        }}
      />
      <div className="w-full max-w-md rounded-2xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] p-8 shadow-xl">
        <h1 className="text-xl font-semibold text-white">Create account</h1>
        <p className="mt-1 text-sm text-slate-400">Start learning with Fraylon Mentor</p>
        <form onSubmit={onSubmit} className="mt-6 space-y-4">
          <div>
            <label className="block text-sm text-slate-400">Name</label>
            <input
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-600 bg-[#0c1222] px-3 py-2 text-white outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-400">Email</label>
            <input
              type="email"
              required
              autoComplete="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-600 bg-[#0c1222] px-3 py-2 text-white outline-none focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm text-slate-400">Password (min 6)</label>
            <input
              type="password"
              required
              minLength={6}
              autoComplete="new-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-600 bg-[#0c1222] px-3 py-2 text-white outline-none focus:border-blue-500"
            />
          </div>
          {err && <p className="text-sm text-red-400">{err}</p>}
          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-lg bg-blue-600 py-2.5 font-medium text-white hover:bg-blue-500 disabled:opacity-50"
          >
            {busy ? "Creating…" : "Register"}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-slate-400">
          Already have an account?{" "}
          <Link to="/login" className="text-blue-400 hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
