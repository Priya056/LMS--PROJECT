import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, type Course } from "../api";

export default function Dashboard() {
  const [courses, setCourses] = useState<Course[] | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    api
      .courses()
      .then(setCourses)
      .catch((e: Error) => setErr(e.message));
  }, []);

  if (err) return <p className="text-red-400">{err}</p>;
  if (!courses) return <p className="text-slate-400">Loading courses…</p>;

  return (
    <div className="w-full overflow-hidden">
      <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-white">Courses</h1>
        <p className="mt-2 max-w-2xl text-slate-400">
          Harvard CS50 Python and CS50 Artificial Intelligence, with{" "}
          <strong className="text-slate-300">Fraylon Mentor</strong> for guidance on every problem.
        </p>
        <ul className="mt-8 grid gap-6 sm:grid-cols-1 lg:grid-cols-2">
          {courses.map((c) => (
            <li key={c.id}>
              <Link
                to={`/course/${c.slug}`}
                className="block h-full rounded-xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] p-6 transition hover:border-blue-500/50 hover:bg-slate-800/40"
              >
                <h2 className="text-lg font-semibold text-white">{c.title}</h2>
                <p className="mt-2 line-clamp-3 text-sm text-slate-400 max-w-full break-words">{c.description}</p>
                <span className="mt-4 inline-block text-sm font-medium text-blue-400">
                  View problems →
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
