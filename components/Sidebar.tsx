"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart3, Clock3, Home, Sparkles } from "lucide-react";

const links = [
  { href: "/", label: "Predict", icon: Home },
  { href: "/history", label: "History", icon: Clock3 },
  { href: "/model", label: "Model", icon: BarChart3 },
];

function isActive(pathname: string, href: string): boolean {
  if (href === "/") return pathname === "/";
  return pathname.startsWith(href);
}

export function Sidebar() {
  const pathname = usePathname();

  return (
    <>
      <aside className="fixed left-0 top-0 hidden h-screen w-[220px] border-r border-[var(--color-border)] bg-[var(--color-bg)]/95 px-4 pb-6 pt-8 backdrop-blur md:flex md:flex-col">
        <div className="mb-8 flex items-center gap-3 px-2">
          <div className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)]">
            <Sparkles className="h-5 w-5 text-[#020617]" />
          </div>
          <span className="text-xl font-bold tracking-tight">HouseIQ</span>
        </div>

        <nav className="flex flex-1 flex-col gap-1">
          {links.map((link) => {
            const Icon = link.icon;
            const active = isActive(pathname, link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`group relative flex items-center gap-3 rounded-xl px-3 py-3 text-sm transition ${
                  active
                    ? "border-l-2 border-[var(--color-accent-primary)] bg-sky-400/10 text-[var(--color-accent-primary)]"
                    : "text-[var(--color-muted)] hover:bg-slate-800/60 hover:text-[var(--color-text)]"
                }`}
              >
                <Icon className="h-4 w-4" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>

        <p className="px-2 text-xs text-[var(--color-muted)]">Powered by ML</p>
      </aside>

      <nav className="fixed bottom-0 left-0 z-40 grid w-full grid-cols-3 border-t border-[var(--color-border)] bg-[var(--color-surface)]/95 backdrop-blur md:hidden">
        {links.map((link) => {
          const Icon = link.icon;
          const active = isActive(pathname, link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex flex-col items-center gap-1 py-3 text-xs ${
                active ? "text-[var(--color-accent-primary)]" : "text-[var(--color-muted)]"
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{link.label}</span>
            </Link>
          );
        })}
      </nav>
    </>
  );
}
