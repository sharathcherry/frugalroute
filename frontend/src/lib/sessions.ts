// Shared session storage utilities — kept outside route files to avoid HMR issues

export type Source = "local" | "remote" | "cache";

export type Msg = {
  id: string;
  role: "user" | "assistant";
  text: string;
  source?: Source;
  model?: string;
  ms?: number;
  tokens?: number;
  cost?: number;
  saved?: number;
  reason?: string;
  confidence?: number;
};

export type ChatSession = {
  id: string;
  title: string;
  ts: number;
  messages: Msg[];
};

const STORAGE_KEY = "frugal_sessions";

export function loadSessions(): ChatSession[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

export function saveSession(session: ChatSession) {
  const sessions = loadSessions();
  const idx = sessions.findIndex((s) => s.id === session.id);
  if (idx >= 0) sessions[idx] = session;
  else sessions.unshift(session);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(sessions.slice(0, 20)));
  window.dispatchEvent(new CustomEvent("frugal_sessions_updated"));
}
