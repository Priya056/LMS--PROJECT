import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "./auth";

function Logo() {
  return (
    <NavLink to="/" className="flex items-center gap-2 flex-shrink-0">
      <img
        src="/logo.png"
        alt="Fraylon Academy"
        className="h-9 w-auto max-w-[220px] object-contain"
        width={200}
        height={40}
        onError={(e) => {
          const el = e.currentTarget;
          if (el.src.endsWith("/logo.svg")) return;
          el.src = "/logo.svg";
        }}
      />
    </NavLink>
  );
}

export default function Shell() {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen w-full overflow-x-hidden flex flex-col">
      <header className="border-b border-[var(--color-fa-border)] bg-[var(--color-fa-surface)]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3 w-full">
          <Logo />
          <nav className="flex items-center gap-4 text-sm overflow-x-auto">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                isActive ? "font-medium text-blue-400 whitespace-nowrap" : "text-slate-400 hover:text-white whitespace-nowrap"
              }
            >
              Courses
            </NavLink>
            <span className="text-slate-500 flex-shrink-0">|</span>
            <span className="text-slate-300 truncate">{user?.name}</span>
            <button
              type="button"
              onClick={logout}
              className="rounded-lg border border-slate-600 px-3 py-1.5 text-slate-300 hover:bg-slate-800 transition-colors flex-shrink-0 whitespace-nowrap"
            >
              Sign out
            </button>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-8 w-full flex-1 overflow-x-hidden">
        <Outlet />
      </main>
    </div>
  );
}
