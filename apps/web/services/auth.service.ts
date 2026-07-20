import { apiClient } from "@/lib/api-client";
import type { LoginRequest, TokenResponse } from "@/types/auth";

class AuthService {
  async login(request: LoginRequest) {
    return (await apiClient.post<TokenResponse>("/auth/login", request)).data;
  }
}

export const authService = new AuthService();
