import type { Metadata } from "next";
import { IBM_Plex_Mono, IBM_Plex_Sans } from "next/font/google";
import { Info } from "lucide-react";

import "@/app/globals.css";

const plexSans = IBM_Plex_Sans({
  variable: "--font-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"]
});

const plexMono = IBM_Plex_Mono({
  variable: "--font-mono",
  subsets: ["latin"],
  weight: ["400", "500", "600"]
});

export const metadata: Metadata = {
  title: "Forgery Detection Forensic Platform",
  description: "Case-based multi-modal digital forgery detection for images and documents."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="dark">
      <body className={`${plexSans.variable} ${plexMono.variable} relative flex min-h-screen flex-col bg-background font-sans text-text`}>
        <div className="absolute right-6 top-8 z-50 group">
           <Info className="h-5 w-5 text-muted transition-colors hover:text-accent cursor-help" />
           <div className="absolute right-0 top-8 w-80 invisible opacity-0 rounded-xl border border-border bg-panel p-5 shadow-2xl transition-all duration-300 group-hover:visible group-hover:opacity-100">
               <h3 className="text-sm font-semibold text-text">MCA Master's Project</h3>
               <p className="mt-2 text-xs leading-relaxed text-muted">
                  ForensIQ was developed as a comprehensive academic project for a Master of Computer Applications (MCA) degree. It demonstrates hybrid digital forensic methodologies, combining Error Level Analysis, SIFT local feature matching, and heuristic OCR and metadata evaluations into a full-stack Next.js and FastAPI application.
               </p>
               <div className="mt-4 pt-3 border-t border-border/50 text-right">
                 <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-accent/80">
                   Developer: Sarath SK
                 </p>
               </div>
           </div>
        </div>
        <div className="flex-1">
          {children}
        </div>
        <footer className="w-full border-t border-border/40 bg-panel/30 py-6 text-center">
           <p className="text-xs font-medium text-muted/80 px-6">Copy-Move Image Forgery Detection Using SIFT Algorithm with Tampered Region Localization for Digital Image Authentication (Hybrid)</p>
           <p className="mt-2 font-mono text-[10px] uppercase tracking-[0.2em] text-accent/60">MCA Project • Developed by Sarath</p>
        </footer>
      </body>
    </html>
  );
}

