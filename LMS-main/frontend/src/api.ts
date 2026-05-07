const TOKEN_KEY = "fa_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function apiFetch(path: string, init: RequestInit = {}) {
  const token = getToken();
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const res = await fetch(path, { ...init, headers });
  if (res.status === 401) {
    clearToken();
    window.dispatchEvent(new Event("fa:logout"));
  }
  return res;
}

export async function apiJson<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await apiFetch(path, init);
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const j = await res.json();
      if (j.detail) detail = typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail);
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export type Course = { id: number; slug: string; title: string; description: string };
export type ProblemSummary = { id: number; slug: string; title: string; week_label: string; sort_order: number };
export type ProblemDetail = ProblemSummary & {
  course_slug: string;
  description: string;
  check50_slug: string;
};
export type Lecture = { number: number; title: string; content: string };
export type Submission = {
  id: number;
  problem_id: number;
  code: string;
  output: string;
  passed: boolean;
  created_at: string;
};
export type ChatMsg = { role: string; content: string; created_at: string };

export const api = {
  register: (email: string, password: string, name: string) =>
    apiJson<{ access_token: string }>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, name }),
    }),
  login: (email: string, password: string) =>
    apiJson<{ access_token: string }>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  me: () => apiJson<{ id: number; email: string; name: string }>("/api/auth/me"),
  courses: () => apiJson<Course[]>("/api/courses"),
  courseProblems: (slug: string) => apiJson<ProblemSummary[]>(`/api/courses/${slug}/problems`),
  courseLectures: (slug: string) => apiJson<Lecture[]>(`/api/courses/${slug}/lectures`),
  problem: (id: number) => apiJson<ProblemDetail>(`/api/problems/${id}`),
  submit: (problemId: number, code: string) =>
    apiJson<Submission>(`/api/problems/${problemId}/submit`, {
      method: "POST",
      body: JSON.stringify({ code }),
    }),
  chat: (problemId: number, message: string, studentCode: string | null) =>
    apiJson<{ reply: string }>("/api/chat", {
      method: "POST",
      body: JSON.stringify({ problem_id: problemId, message, student_code: studentCode }),
    }),
  chatHistory: (problemId: number) =>
    apiJson<ChatMsg[]>(`/api/problems/${problemId}/chat-history`),
};
