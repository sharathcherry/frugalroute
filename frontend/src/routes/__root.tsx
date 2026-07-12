import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
  useRouterState,
  HeadContent,
  Scripts,
} from "@tanstack/react-router";
import { useEffect, useState, type ReactNode } from "react";
import { Toaster } from "@/components/ui/sonner";
import { Zap, MessageSquare, BarChart3, Settings, Cpu, Plus, Clock, ChevronDown, PanelLeftClose, PanelLeftOpen } from "lucide-react";

import appCss from "../styles.css?url";
import { reportLovableError } from "../lib/lovable-error-reporting";
import { loadSessions, type ChatSession } from "../lib/sessions";

function NotFoundComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="glass max-w-md rounded-2xl p-8 text-center">
        <h1 className="font-mono-tech text-7xl font-bold text-primary text-glow-red">404</h1>
        <p className="mt-4 text-muted-foreground">Route not found in the neural graph.</p>
        <Link to="/" className="mt-6 inline-block rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground glow-red">
          Return home
        </Link>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  const router = useRouter();
  useEffect(() => { reportLovableError(error, { boundary: "root" }); }, [error]);
  return (
    <div className="flex min-h-screen items-center justify-center px-4">
      <div className="glass max-w-md rounded-2xl p-8 text-center">
        <h1 className="text-xl font-semibold">Signal lost</h1>
        <p className="mt-2 text-sm text-muted-foreground">A packet failed to route. Retry?</p>
        <button
          onClick={() => { router.invalidate(); reset(); }}
          className="mt-6 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground glow-red"
        >
          Try again
        </button>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "FrugalRoute — Intelligence Routed. Costs Slashed." },
      { name: "description", content: "Hybrid AI routing that intelligently sends queries to local or cloud models to slash API costs." },
      { property: "og:title", content: "FrugalRoute" },
      { property: "og:description", content: "Hybrid AI routing. Local + cloud. Massive savings." },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
    links: [
      { rel: "stylesheet", href: appCss },
      { rel: "preconnect", href: "https://fonts.googleapis.com" },
      { rel: "preconnect", href: "https://fonts.gstatic.com", crossOrigin: "anonymous" },
      { rel: "stylesheet", href: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" },
      { rel: "icon", href: "/favicon.ico", type: "image/x-icon" },
    ],
  }),
  shellComponent: RootShell,
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootShell({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <head><HeadContent /></head>
      <body>{children}<Scripts /></body>
    </html>
  );
}

const BOTTOM_NAV = [
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/settings", label: "Settings", icon: Settings },
] as const;

function timeAgo(ts: number) {
  const diff = Date.now() - ts;
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

function Sidebar() {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [recentOpen, setRecentOpen] = useState(false);
  const [collapsed, setCollapsed] = useState(false);

  // Load sessions from localStorage and refresh when updated; restore collapse pref
  useEffect(() => {
    const refresh = () => setSessions(loadSessions());
    refresh();
    try { setCollapsed(localStorage.getItem("frugal_sidebar_collapsed") === "1"); } catch { /* ignore */ }
    window.addEventListener("frugal_sessions_updated", refresh);
    return () => window.removeEventListener("frugal_sessions_updated", refresh);
  }, []);

  const toggleCollapsed = () =>
    setCollapsed((c) => {
      const next = !c;
      try { localStorage.setItem("frugal_sidebar_collapsed", next ? "1" : "0"); } catch { /* ignore */ }
      if (next) setRecentOpen(false);
      return next;
    });

  const navRow = (to: string, label: string, Icon: typeof Zap, active: boolean) => (
    <Link
      key={to}
      to={to}
      title={collapsed ? label : undefined}
      className={`group flex items-center rounded-lg text-sm transition-all ${
        collapsed ? "justify-center px-0 py-2.5" : "gap-3 px-3 py-2.5"
      } ${
        active
          ? "bg-primary/15 text-foreground glow-red"
          : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
      }`}
    >
      <Icon className={`h-4 w-4 shrink-0 ${active ? "text-primary" : ""}`} />
      {!collapsed && <span className="truncate">{label}</span>}
      {!collapsed && active && <span className="ml-auto h-1.5 w-1.5 rounded-full bg-primary animate-pulse-dot" />}
    </Link>
  );

  return (
    <aside
      className={`glass-strong sticky top-0 z-40 flex h-screen w-full shrink-0 flex-col border-r border-border/60 p-3 transition-[width] duration-200 ${
        collapsed ? "md:w-16" : "md:w-64"
      }`}
    >
      {/* Logo + collapse toggle */}
      <div className={`mb-4 flex items-center py-3 ${collapsed ? "justify-center px-0" : "gap-2 px-2"}`}>
        <div className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-primary glow-red">
          <Cpu className="h-5 w-5 text-primary-foreground" />
        </div>
        {!collapsed && (
          <div className="min-w-0 flex-1">
            <div className="font-mono-tech text-sm font-bold tracking-wider">FRUGAL<span className="text-primary">ROUTE</span></div>
            <div className="text-[10px] uppercase tracking-widest text-muted-foreground">Hybrid AI Router</div>
          </div>
        )}
        {!collapsed && (
          <button
            type="button"
            onClick={toggleCollapsed}
            title="Collapse sidebar"
            className="grid h-7 w-7 shrink-0 place-items-center rounded-md text-muted-foreground hover:bg-white/5 hover:text-foreground"
          >
            <PanelLeftClose className="h-4 w-4" />
          </button>
        )}
      </div>

      {/* Expand button (collapsed only) */}
      {collapsed && (
        <button
          type="button"
          onClick={toggleCollapsed}
          title="Expand sidebar"
          className="mb-3 grid h-9 place-items-center rounded-lg text-muted-foreground hover:bg-white/5 hover:text-foreground"
        >
          <PanelLeftOpen className="h-4 w-4" />
        </button>
      )}

      {/* New Chat button */}
      <Link
        to="/chat"
        title={collapsed ? "New Chat" : undefined}
        className={`mb-3 flex items-center rounded-lg border border-border/40 bg-white/[0.03] text-sm font-medium text-muted-foreground hover:bg-primary/10 hover:text-primary hover:border-primary/30 transition-colors ${
          collapsed ? "justify-center py-2.5" : "gap-2 px-3 py-2.5"
        }`}
      >
        <Plus className="h-4 w-4 shrink-0" />
        {!collapsed && "New Chat"}
      </Link>

      {/* Recent — nav item with a dropdown to select between chats */}
      <div className={`mt-1 flex min-h-0 flex-col ${recentOpen && !collapsed ? "flex-1" : ""}`}>
        <button
          type="button"
          title={collapsed ? "Recent chats" : undefined}
          onClick={() => { if (collapsed) { toggleCollapsed(); setRecentOpen(true); } else setRecentOpen((v) => !v); }}
          aria-expanded={recentOpen}
          className={`group flex items-center rounded-lg text-sm transition-all ${
            collapsed ? "justify-center px-0 py-2.5" : "gap-3 px-3 py-2.5"
          } ${
            recentOpen && !collapsed ? "bg-white/5 text-foreground" : "text-muted-foreground hover:bg-white/5 hover:text-foreground"
          }`}
        >
          <Clock className="h-4 w-4 shrink-0" />
          {!collapsed && <span className="truncate">Recent</span>}
          {!collapsed && sessions.length > 0 && (
            <span className="ml-auto rounded-full bg-white/10 px-1.5 text-[10px] font-mono-tech text-muted-foreground">
              {sessions.length}
            </span>
          )}
          {!collapsed && (
            <ChevronDown
              className={`${sessions.length > 0 ? "ml-1.5" : "ml-auto"} h-4 w-4 shrink-0 transition-transform ${
                recentOpen ? "rotate-180" : ""
              }`}
            />
          )}
        </button>

        {recentOpen && !collapsed && (
          <div className="sidebar-scroll mt-1 ml-3 flex min-h-0 flex-1 flex-col gap-0.5 overflow-y-auto border-l border-border/40 pl-2 [scrollbar-width:thin] [&::-webkit-scrollbar]:w-1.5 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:rounded-full [&::-webkit-scrollbar-thumb]:bg-white/15 hover:[&::-webkit-scrollbar-thumb]:bg-white/25">
            {sessions.length === 0 && (
              <div className="px-3 py-2 text-xs text-muted-foreground/60">No chats yet</div>
            )}
            {sessions.map((s) => (
              <Link
                key={s.id}
                to="/chat"
                search={{ session: s.id }}
                onClick={() => setRecentOpen(false)}
                className="group flex items-start gap-2 rounded-lg px-3 py-2 text-xs text-muted-foreground hover:bg-white/5 hover:text-foreground transition-colors"
              >
                <MessageSquare className="h-3 w-3 mt-0.5 shrink-0" />
                <div className="min-w-0 flex-1">
                  <div className="truncate">{s.title}</div>
                  <div className="font-mono-tech text-[10px] text-muted-foreground/60">{timeAgo(s.ts)}</div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Bottom nav — Analytics & Settings pinned above status */}
      <nav className={`flex flex-col gap-1 mb-3 ${recentOpen && !collapsed ? "" : "mt-auto"}`}>
        {BOTTOM_NAV.map(({ to, label, icon: Icon }) => navRow(to, label, Icon, pathname === to))}
      </nav>

      {/* Local node status — bottom */}
      <div className={`glass rounded-xl ${collapsed ? "grid place-items-center p-2" : "p-3"}`}>
        {collapsed ? (
          <span className="relative flex h-2.5 w-2.5" title="Local node online">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-400" />
          </span>
        ) : (
          <>
            <div className="flex items-center gap-2 text-xs">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-400" />
              </span>
              <span className="font-mono-tech text-muted-foreground">LOCAL NODE ONLINE</span>
            </div>
            <div className="mt-1 font-mono-tech text-[10px] text-muted-foreground">Qwen 3B &middot; 12ms avg</div>
          </>
        )}
      </div>
    </aside>
  );
}

function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  return (
    <QueryClientProvider client={queryClient}>
      <div className="flex min-h-screen w-full flex-col md:flex-row">
        <Sidebar />
        <main className="flex-1 min-w-0">
          <Outlet />
        </main>
      </div>
      <Toaster theme="dark" position="top-right" />
    </QueryClientProvider>
  );
}
