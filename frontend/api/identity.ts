import { apiRequest } from "./client";

export interface LoginRequest {
  email: string;
  password: string;
  remember_me: boolean;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_at: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface RefreshTokenResponse {
  access_token: string;
  refresh_token: string;
  expires_at: string;
}

export interface LogoutRequest {
  refresh_token: string;
}

export interface AuthenticationResponse {
  success: boolean;
  message: string;
}

export function login(
  request: LoginRequest,
): Promise<LoginResponse> {
  return apiRequest<LoginResponse>(
    "/identity/authentication/login",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export function refreshToken(
  request: RefreshTokenRequest,
): Promise<RefreshTokenResponse> {
  return apiRequest<RefreshTokenResponse>(
    "/identity/authentication/refresh",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}

export function logout(
  request: LogoutRequest,
): Promise<AuthenticationResponse> {
  return apiRequest<AuthenticationResponse>(
    "/identity/authentication/logout",
    {
      method: "POST",
      body: JSON.stringify(request),
    },
  );
}