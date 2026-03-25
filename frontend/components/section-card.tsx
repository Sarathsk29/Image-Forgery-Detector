import React from "react";
import { cn } from "@/lib/utils";

export function SectionCard({
  className,
  title,
  eyebrow,
  children
}: {
  className?: string;
  title: string;
  eyebrow?: string;
  children: React.ReactNode;
}) {
  return (
    <section className={cn("rounded-2xl border border-border bg-surface/90 p-5 shadow-panel backdrop-blur", className)}>
      <div className="mb-4 flex items-center justify-between gap-3">
        <div>
          {eyebrow ? <p className="font-mono text-xs uppercase tracking-[0.3em] text-accent/80">{eyebrow}</p> : null}
          <h2 className="mt-1 text-xl font-semibold text-text">{title}</h2>
        </div>
      </div>
      {children}
    </section>
  );
}

