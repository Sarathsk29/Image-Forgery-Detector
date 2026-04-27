"use client";

import { useEffect, useState, use } from "react";
import { ReportView } from "@/components/report-view";
import { LoaderCircle } from "lucide-react";

export default function ReportPage({ params }: { params: Promise<{ jobId: string }> }) {
  const { jobId } = use(params);
  const [session, setSession] = useState<{caseId: string; accessKey: string} | null>(null);
  
  useEffect(() => {
    const stored = window.localStorage.getItem("forensiq_session");
    if (stored) {
      try {
        setSession(JSON.parse(stored));
      } catch {}
    }
  }, []);

  if (!session) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="rounded-2xl border border-border bg-surface/90 p-6 text-center shadow-xl">
          <LoaderCircle className="mx-auto h-8 w-8 animate-spin text-accent" />
          <p className="mt-4 font-mono text-xs uppercase tracking-[0.3em] text-accent/80">Authenticating Session...</p>
        </div>
      </div>
    );
  }

  return <ReportView caseId={session.caseId} jobId={jobId} accessKey={session.accessKey} />;
}
