"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { loadRecentCases, type RecentCase } from "@/lib/recent-cases";
import { Button } from "@/components/ui/button";
import { SectionCard } from "@/components/section-card";
import { StatusBadge } from "@/components/status-badge";


export function CaseListShell() {
  const [cases, setCases] = useState<RecentCase[]>([]);

  useEffect(() => {
    setCases(loadRecentCases());
  }, []);

  return (
    <main className="mx-auto min-h-screen max-w-6xl px-6 py-10">
      <div className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.36em] text-accent/80">Case List</p>
          <h1 className="mt-3 text-4xl font-semibold text-white">Recently Accessed Investigations</h1>
          <p className="mt-3 max-w-2xl text-sm leading-7 text-muted">
            This list is stored only in the current browser to match the public no-login workflow. Use it as a quick way to reopen recent cases.
          </p>
        </div>
        <Button asChild>
          <Link href="/">Create or Open Case</Link>
        </Button>
      </div>

      <SectionCard title="Recent Cases" eyebrow="Local History">
        {cases.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-border bg-panel/40 p-8 text-center text-sm text-muted">
            No local cases found yet. Create or open a case first to populate this page.
          </div>
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {cases.map((entry) => (
              <article key={entry.caseId} className="rounded-2xl border border-border bg-panel/60 p-5">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="font-mono text-xs uppercase tracking-[0.28em] text-accent/80">{entry.caseId}</p>
                    <h2 className="mt-2 text-xl font-semibold text-white">{entry.title || "Untitled Case"}</h2>
                  </div>
                  <StatusBadge value={entry.status} />
                </div>
                <p className="mt-4 text-sm text-muted">Last opened: {new Date(entry.accessedAt).toLocaleString()}</p>
                <p className="mt-2 font-mono text-xs text-muted">Access Key: {entry.accessKey}</p>
                <Button asChild className="mt-5">
                  <Link href={`/cases/${entry.caseId}?accessKey=${encodeURIComponent(entry.accessKey)}`}>Open Case Workspace</Link>
                </Button>
              </article>
            ))}
          </div>
        )}
      </SectionCard>
    </main>
  );
}

