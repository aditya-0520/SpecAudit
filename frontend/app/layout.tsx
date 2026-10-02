import type { Metadata } from "next";
import "./globals.css";
import "./design-system.css";
export const metadata: Metadata = { title: "SpecAudit-IS | Tender intelligence, made auditable", description: "AI-assisted tender auditing with evidence, registry verification and officer approval." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="en"><body>{children}</body></html>; }
