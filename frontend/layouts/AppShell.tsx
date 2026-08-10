import type { ReactNode } from "react";
import { Sidebar } from "../components/navigation/Sidebar";

type AppShellProps = {
  children: ReactNode;
};

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="qwos-app">
      <Sidebar />

      <main className="qwos-main">
        {children}
      </main>
    </div>
  );
}