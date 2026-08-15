import type { ReactNode } from "react";
import { Sidebar } from "../components/navigation/Sidebar";

type AppShellProps = {
  children: ReactNode;
  onLogout: () => void;
};

export function AppShell({
  children,
  onLogout,
}: AppShellProps) {
  return (
    <div className="qwos-app">
      <Sidebar onLogout={onLogout} />

      <main className="qwos-main">
        {children}
      </main>
    </div>
  );
}