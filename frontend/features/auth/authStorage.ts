import type {
  LoginResponse,
  RefreshTokenResponse,
} from "../../api/identity";

const ACCESS_TOKEN_KEY = "qwos_access_token";
const REFRESH_TOKEN_KEY = "qwos_refresh_token";
const EXPIRES_AT_KEY = "qwos_token_expires_at";

export function saveAuthentication(
  response: LoginResponse | RefreshTokenResponse,
): void {
  localStorage.setItem(
    ACCESS_TOKEN_KEY,
    response.access_token,
  );

  localStorage.setItem(
    REFRESH_TOKEN_KEY,
    response.refresh_token,
  );

  localStorage.setItem(
    EXPIRES_AT_KEY,
    response.expires_at,
  );
}

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getTokenExpiresAt(): string | null {
  return localStorage.getItem(EXPIRES_AT_KEY);
}

export function clearAuthentication(): void {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(EXPIRES_AT_KEY);
}

export function isAuthenticated(): boolean {
  const accessToken = getAccessToken();
  const expiresAt = getTokenExpiresAt();

  if (!accessToken || !expiresAt) {
    return false;
  }

  const expiration = Date.parse(expiresAt);

  if (Number.isNaN(expiration)) {
    return false;
  }

  return expiration > Date.now();
}