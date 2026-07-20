"use client";

import { createContext, ReactNode, useCallback, useContext, useSyncExternalStore } from "react";

import { authService } from "@/services";
import { clearStoredToken, getStoredToken, setStoredToken, subscribeToToken } from "@/lib/auth-storage";

function getServerSnapshot() {
  return null;
}

interface AuthContextValue {
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const token = useSyncExternalStore(subscribeToToken, getStoredToken, getServerSnapshot);

  const login = useCallback(async (email: string, password: string) => {
    const response = await authService.login({ email, password });
    setStoredToken(response.access_token);
  }, []);

  const logout = useCallback(() => {
    clearStoredToken();
  }, []);

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: Boolean(token), login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
