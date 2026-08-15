import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  login as loginApi,
  logout as logoutApi,
} from "../../api/identity";

import type {
  AuthContextValue,
  AuthTokens,
} from "./auth.types";

const AuthContext = createContext<AuthContextValue | undefined>(
  undefined,
);

type AuthProviderProps = {
  children: ReactNode;
};

function toAuthTokens(response: {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_at: string;
}): AuthTokens {
  return {
    accessToken: response.access_token,
    refreshToken: response.refresh_token,
    tokenType: response.token_type,
    expiresAt: response.expires_at,
  };
}

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [tokens, setTokens] = useState<AuthTokens | null>(
    null,
  );

  const [isLoading, setIsLoading] = useState(false);

  const login = useCallback(
    async (
      email: string,
      password: string,
      rememberMe = false,
    ) => {
      setIsLoading(true);

      try {
        const response = await loginApi({
          email,
          password,
          remember_me: rememberMe,
        });

        setTokens(toAuthTokens(response));
      } finally {
        setIsLoading(false);
      }
    },
    [],
  );

  const logout = useCallback(async () => {
    if (!tokens) {
      return;
    }

    setIsLoading(true);

    try {
      await logoutApi({
        refresh_token: tokens.refreshToken,
      });
    } finally {
      setTokens(null);
      setIsLoading(false);
    }
  }, [tokens]);

  const value = useMemo<AuthContextValue>(
    () => ({
      isAuthenticated: tokens !== null,
      isLoading,
      tokens,
      login,
      logout,
    }),
    [isLoading, login, logout, tokens],
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used within an AuthProvider",
    );
  }

  return context;
}
