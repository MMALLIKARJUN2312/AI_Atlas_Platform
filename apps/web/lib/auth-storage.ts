const TOKEN_KEY = "ai-atlas-admin-token";

const listeners = new Set<() => void>();

function notify() {
  listeners.forEach((listener) => listener());
}

export function subscribeToToken(listener: () => void) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function getStoredToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string): void {
  window.localStorage.setItem(TOKEN_KEY, token);
  notify();
}

export function clearStoredToken(): void {
  window.localStorage.removeItem(TOKEN_KEY);
  notify();
}
