import { useEffect, useState, type ReactNode } from "react";
import { Link, useParams } from "react-router-dom";
import { api, type Lecture } from "../api";

function SimpleMarkdown({ content }: { content: string }) {
  const lines = content.split("\n");
  const elements: ReactNode[] = [];
  let listItems: ReactNode[] = [];
  let inCodeBlock = false;
  let codeLines: string[] = [];

  const flushList = () => {
    if (listItems.length > 0) {
      elements.push(
        <ul key={`list-${elements.length}`} className="ml-6 list-disc text-slate-300 space-y-1">
          {listItems}
        </ul>
      );
      listItems = [];
    }
  };

  const flushCode = () => {
    if (codeLines.length > 0) {
      elements.push(
        <pre
          key={`code-${elements.length}`}
          className="rounded-lg bg-slate-950 p-4 text-sm text-slate-200 overflow-x-auto"
        >
          <code>{codeLines.join("\n")}</code>
        </pre>
      );
      codeLines = [];
    }
  };

  lines.forEach((line, i) => {
    const trimmed = line.trim();

    if (trimmed.startsWith("```") || trimmed.startsWith("~~~")) {
      if (inCodeBlock) {
        flushCode();
      }
      inCodeBlock = !inCodeBlock;
      return;
    }

    if (inCodeBlock) {
      codeLines.push(line.replace(/\t/g, "  "));
      return;
    }

    if (trimmed.startsWith("# ")) {
      flushList();
      flushCode();
      elements.push(
        <h1 key={i} className="text-3xl font-bold text-white mt-8 mb-4 border-b border-slate-700 pb-2">
          {trimmed.replace(/^#\s+/, "")}
        </h1>
      );
      return;
    }

    if (trimmed.startsWith("## ")) {
      flushList();
      flushCode();
      elements.push(
        <h2 key={i} className="text-2xl font-semibold text-white mt-6 mb-3">
          {trimmed.replace(/^##\s+/, "")}
        </h2>
      );
      return;
    }

    if (trimmed.startsWith("### ")) {
      flushList();
      flushCode();
      elements.push(
        <h3 key={i} className="text-xl font-medium text-white mt-5 mb-2">
          {trimmed.replace(/^###\s+/, "")}
        </h3>
      );
      return;
    }

    if (trimmed.length === 0) {
      flushList();
      flushCode();
      elements.push(<div key={`spacer-${i}`} className="h-3" />);
      return;
    }

    if (trimmed.startsWith("- ") || trimmed.startsWith("* ") || /^\d+\.\s/.test(trimmed)) {
      const text = trimmed.replace(/^[-*]\s+/, "").replace(/^\d+\.\s+/, "");
      listItems.push(
        <li key={`li-${i}`} className="text-slate-300">
          {text}
        </li>
      );
      return;
    }

    flushList();
    flushCode();
    elements.push(
      <p key={i} className="text-slate-300 leading-relaxed">
        {line}
      </p>
    );
  });

  flushList();
  flushCode();

  return <div className="space-y-3">{elements}</div>;
}

export default function LecturePage() {
  const { slug, number } = useParams<{ slug: string; number: string }>();
  const [lecture, setLecture] = useState<Lecture | null>(null);
  const [err, setErr] = useState<string | null>(null);

  useEffect(() => {
    if (!slug || !number) return;
    api
      .courseLectures(slug)
      .then((lectures) => {
        const lectureNumber = Number(number);
        const found = lectures.find((l) => l.number === lectureNumber);
        if (found) {
          setLecture(found);
          setErr(null);
        } else {
          setLecture(null);
          setErr("Lecture not found");
        }
      })
      .catch((e: Error) => {
        setLecture(null);
        setErr(e.message);
      });
  }, [slug, number]);
  if (err) return <p className="text-red-400 p-8">{err}</p>;
  if (!lecture) return <div className="p-8 text-slate-400">Loading…</div>;

  return (
    <div className="mx-auto max-w-4xl p-6">
      <Link to={`/course/${slug}`} className="text-sm text-blue-400 hover:underline mb-6 inline-block">
        ← Back to {slug === "cs50ai" ? "CS50 AI" : slug === "cs50p" ? "CS50 Python" : "Course"}
      </Link>
      
      <div className="rounded-xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] p-8">
        <SimpleMarkdown content={lecture.content} />
      </div>
    </div>
  );
}
