import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, type Lecture } from "../api";

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
    <div className="w-full overflow-hidden">
      <div className="mx-auto w-full max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
        <Link 
          to={`/course/${slug}`} 
          className="text-sm text-blue-400 hover:underline mb-6 inline-block transition-colors hover:text-blue-300"
        >
          ← Back to {slug === "cs50ai" ? "CS50 AI" : slug === "cs50p" ? "CS50 Python" : "Course"}
        </Link>
        
        <div className="rounded-xl border border-[var(--color-fa-border)] bg-[var(--color-fa-surface)] p-6 sm:p-8">
          <div 
            className="markdown-content prose prose-invert prose-blue max-w-none overflow-hidden"
            style={{
              wordWrap: "break-word",
              overflowWrap: "break-word",
            }}
            dangerouslySetInnerHTML={{ __html: (window as any).marked.parse(lecture.content) }} 
          />
        </div>
      </div>
    </div>
  );
}
