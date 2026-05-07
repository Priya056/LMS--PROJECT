import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, type ChatMsg, type ProblemDetail, type Submission } from "../api";

export default function ProblemPage() {
  const { id } = useParams<{ id: string }>();
  const pid = Number(id);
  const [problem, setProblem] = useState<ProblemDetail | null>(null);
  const [code, setCode] = useState(`# Your solution for this problem\n`);
  const [submission, setSubmission] = useState<Submission | null>(null);
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [chatErr, setChatErr] = useState<string | null>(null);
  const [chatBusy, setChatBusy] = useState(false);
  const [submitBusy, setSubmitBusy] = useState(false);
  const [loadErr, setLoadErr] = useState<string | null>(null);

  useEffect(() => {
    if (!Number.isFinite(pid)) return;
    api
      .problem(pid)
      .then((p) => {
        setProblem(p);
        setCode(`# ${p.title}\n\n`);
      })
      .catch((e: Error) => setLoadErr(e.message));
  }, [pid]);

  useEffect(() => {
    if (!Number.isFinite(pid)) return;
    api.chatHistory(pid).then(setMessages).catch(() => setMessages([]));
  }, [pid]);

  async function onSubmitCode() {
    if (!problem) return;
    setSubmitBusy(true);
    try {
      const s = await api.submit(problem.id, code);
      setSubmission(s);
    } catch (e) {
      setLoadErr(e instanceof Error ? e.message : "Submit failed");
    } finally {
      setSubmitBusy(false);
    }
  }

  async function onSendChat() {
    if (!problem || !chatInput.trim()) return;
    setChatErr(null);
    setChatBusy(true);
    const userText = chatInput.trim();
    setChatInput("");
    try {
      await api.chat(problem.id, userText, code);
      const hist = await api.chatHistory(problem.id);
      setMessages(hist);
    } catch (e) {
      setChatErr(e instanceof Error ? e.message : "Chat failed");
      try {
        const hist = await api.chatHistory(problem.id);
        setMessages(hist);
      } catch {
        /* ignore */
      }
    } finally {
      setChatBusy(false);
    }
  }

  if (!Number.isFinite(pid)) return <p className="text-red-400">Invalid problem</p>;
  if (loadErr && !problem) return <p className="text-red-400">{loadErr}</p>;
  if (!problem) return <p className="text-slate-400">Loading problem…</p>;

  return (
    <div>
      <Link to={`/course/${problem.course_slug}`} className="text-sm text-blue-400 hover:underline">
        ← Back to course
      </Link>
      <div className="mt-4 lg:grid lg:grid-cols-2 lg:gap-8">
        <div>
          <h1 className="text-2xl font-semibold text-white">{problem.title}</h1>
          <p className="mt-1 text-sm text-slate-500">
            {problem.week_label} · check50:{" "}
            <code className="text-slate-400">{problem.check50_slug}</code>
          </p>
          <div className="mt-4 rounded-xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] p-4">
            <h2 className="text-sm font-medium uppercase tracking-wide text-slate-500">
              Description
            </h2>
            <pre className="mt-2 whitespace-pre-wrap font-sans text-sm leading-relaxed text-slate-300">
              {problem.description}
            </pre>
          </div>
          <div className="mt-4">
            <label htmlFor="problem-code" className="text-sm font-medium text-slate-400">
              Your code
            </label>
            <textarea
              id="problem-code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck={false}
              placeholder="# Write your solution here"
              className="font-mono mt-2 min-h-[240px] w-full resize-y rounded-lg border border-slate-600 bg-[#0a0f1a] p-3 text-sm text-slate-200 outline-none focus:border-blue-500"
            />
            <button
              type="button"
              onClick={onSubmitCode}
              disabled={submitBusy}
              className="mt-3 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-500 disabled:opacity-50"
            >
              {submitBusy ? "Running checks…" : "Submit (demo check)"}
            </button>
            {submission && (
              <div className="mt-4 rounded-lg border border-slate-600 bg-[#0a0f1a] p-3">
                <p className={`text-sm font-medium ${submission.passed ? "text-emerald-400" : "text-amber-400"}`}>
                  {submission.passed ? "Checks passed (syntax)" : "Checks failed"}
                </p>
                <pre className="mt-2 max-h-40 overflow-auto font-mono text-xs text-slate-400">
                  {submission.output}
                </pre>
              </div>
            )}
          </div>
        </div>

        <div className="mt-10 lg:mt-0">
          <div className="rounded-xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] lg:sticky lg:top-8">
            <div className="border-b border-[var(--color-fa-border)] px-4 py-3">
              <h2 className="font-semibold text-white">Fraylon Mentor</h2>
              <p className="text-xs text-slate-500">
                AI tutor — asks questions first; configure OPENAI_API_KEY on the server for live replies.
              </p>
            </div>
            <div className="max-h-[min(70vh,540px)] space-y-3 overflow-y-auto p-4">
              {messages.length === 0 && (
                <p className="text-sm text-slate-500">
                  Ask about the problem or your approach. Your latest code is included in context when you
                  message (see agent_prompt.md runtime injection).
                </p>
              )}
              {messages.map((m, i) => (
                <div
                  key={`${m.created_at}-${i}`}
                  className={`rounded-lg px-3 py-2 text-sm ${
                    m.role === "user"
                      ? "ml-4 bg-blue-900/40 text-slate-200"
                      : "mr-4 bg-slate-800/80 text-slate-200"
                  }`}
                >
                  <span className="mb-1 block text-xs font-medium uppercase text-slate-500">
                    {m.role === "user" ? "You" : "Mentor"}
                  </span>
                  <div className="whitespace-pre-wrap">{m.content}</div>
                </div>
              ))}
            </div>
            {chatErr && <p className="border-t border-red-900/50 px-4 py-2 text-sm text-red-400">{chatErr}</p>}
            <div className="flex gap-2 border-t border-[var(--color-fa-border)] p-3">
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && (e.preventDefault(), onSendChat())}
                placeholder="Ask the mentor…"
                className="min-w-0 flex-1 rounded-lg border border-slate-600 bg-[#0a0f1a] px-3 py-2 text-sm text-white outline-none focus:border-blue-500"
              />
              <button
                type="button"
                disabled={chatBusy}
                onClick={onSendChat}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-50"
              >
                {chatBusy ? "…" : "Send"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
