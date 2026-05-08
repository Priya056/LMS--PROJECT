import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, type ProblemSummary, type Lecture } from "../api";

export default function CoursePage() {
  const { slug } = useParams<{ slug: string }>();
  const [problems, setProblems] = useState<ProblemSummary[] | null>(null);
  const [lectures, setLectures] = useState<Lecture[] | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    api
      .courseProblems(slug)
      .then(setProblems)
      .catch((e: Error) => setErr(e.message));
    api
      .courseLectures(slug)
      .then(setLectures)
      .catch(() => setLectures([])); // Ignore errors for lectures
  }, [slug]);

  if (!slug) return null;
  if (err) return <p className="text-red-400">{err}</p>;
  if (!problems) return <p className="text-slate-400">Loading…</p>;

  return (
    <div className="w-full overflow-hidden">
      <div className="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
        <Link to="/" className="text-sm text-blue-400 hover:underline transition-colors hover:text-blue-300">
          ← Courses
        </Link>
        <h1 className="mt-4 text-2xl font-semibold capitalize text-white">
          {slug === "cs50p" ? "CS50 Python" : slug === "cs50ai" ? "CS50 AI" : slug}
        </h1>
        <p className="mt-2 text-slate-400 max-w-2xl">Select a problem to work on with Fraylon Mentor.</p>
        <ul className="mt-6 divide-y divide-slate-700/80 rounded-xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] overflow-hidden">
          {problems.map((p) => (
            <li key={p.id}>
              <Link
                to={`/problem/${p.id}`}
                className="flex items-center justify-between gap-4 px-4 py-4 hover:bg-slate-800/40 transition-colors"
              >
                <div className="min-w-0 flex-1">
                  <span className="block font-medium text-white truncate">{p.title}</span>
                  <span className="text-sm text-slate-500">{p.week_label}</span>
                </div>
                <span className="text-sm text-blue-400 whitespace-nowrap">Open →</span>
              </Link>
            </li>
          ))}
        </ul>
        {lectures && lectures.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-white">Lectures</h2>
            <div className="mt-4 space-y-4">
              {lectures.map((lecture) => (
                <Link
                  key={lecture.number}
                  to={`/course/${slug}/lecture/${lecture.number}`}
                  className="block rounded-xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] p-4 transition hover:bg-slate-800/40 hover:border-blue-500/50"
                >
                  <div className="flex items-center justify-between gap-4">
                    <h3 className="text-lg font-medium text-white truncate">Lecture {lecture.number}: {lecture.title}</h3>
                    <span className="text-sm text-blue-400 whitespace-nowrap">View notes →</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
