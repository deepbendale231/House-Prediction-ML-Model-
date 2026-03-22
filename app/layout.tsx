import type { Metadata } from "next";
import { DM_Sans, Sora } from "next/font/google";

import "./globals.css";
import { Sidebar } from "@/components/Sidebar";

const sora = Sora({
  subsets: ["latin"],
  variable: "--font-sora",
  weight: ["600", "700", "800"],
});

const dmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-dm",
  weight: ["400", "500", "700"],
});

export const metadata: Metadata = {
  title: "HouseIQ",
  description: "California House Price Predictor",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${sora.variable} ${dmSans.variable}`}>
      <body>
        <div className="fixed left-0 top-0 z-50 h-1 w-full bg-gradient-to-r from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)]" />
        <Sidebar />
        <main className="min-h-screen pb-20 pt-10 md:ml-[220px] md:pb-8">{children}</main>
      </body>
    </html>
  );
}
