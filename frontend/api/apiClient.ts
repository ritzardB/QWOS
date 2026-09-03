import { clearAuthentication, getAccessToken } from "../features/auth/authStorage";

export function getAuthenticatedHeaders(
  headers: HeadersInit = {},
): HeadersInit {
  const accessToken = getAccessToken();

  console.log(
    "AUTH DEBUG:",
    accessToken
      ? "Access token exists"
      : "NO ACCESS TOKEN",
  );

  return {
    Accept: "application/json",
    ...headers,
    ...(accessToken
      ? {
          Authorization: `Bearer ${accessToken}`,
        }
      : {}),
  };
}

export function handleAuthenticationFailure(
  response: Response,
): void {
  if (response.status === 401) {
    clearAuthentication();
  }
}