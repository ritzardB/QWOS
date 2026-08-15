import { useState } from "react";
import type { FormEvent } from "react";

import { login } from "../../../api/identity";
import {
  saveAuthentication,
} from "../authStorage";

type LoginPageProps = {
  onLoginSuccess: () => void;
};

export function LoginPage({
  onLoginSuccess,
}: LoginPageProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [rememberMe, setRememberMe] = useState(false);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    setErrorMessage("");
    setIsSubmitting(true);

    try {
      const response = await login({
        email,
        password,
        remember_me: rememberMe,
      });

      saveAuthentication(response);

      onLoginSuccess();
    } catch (error) {
      if (error instanceof Error) {
        setErrorMessage(error.message);
      } else {
        setErrorMessage(
          "Unable to sign in. Please try again.",
        );
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="qwos-login-page">
      <section className="qwos-login-card">
        <div className="qwos-login-brand">
          <div className="qwos-brand-mark">Q</div>

          <div>
            <h1 className="qwos-brand-name">QWOS</h1>
            <p className="qwos-brand-subtitle">
              Quantum Workforce OS
            </p>
          </div>
        </div>

        <div className="qwos-login-heading">
          <p className="qwos-eyebrow">
            Quantum Workforce OS
          </p>

          <h2>Welcome back!</h2>

          <p>
            Sign in to access your workforce operations.
          </p>
        </div>

        <form
          className="qwos-login-form"
          onSubmit={handleSubmit}
        >
          <label htmlFor="email">
            Email address
          </label>

          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
            placeholder="you@example.com"
            required
          />

          <label htmlFor="password">
            Password
          </label>

          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            placeholder="Enter your password"
            minLength={8}
            required
          />

          <label className="qwos-login-remember">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(event) =>
                setRememberMe(event.target.checked)
              }
            />

            <span>Remember me</span>
          </label>

          {errorMessage && (
            <div
              className="qwos-login-error"
              role="alert"
            >
              {errorMessage}
            </div>
          )}

          <button
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting
              ? "Signing in..."
              : "Sign in"}
          </button>
        </form>
      </section>
    </main>
  );
}