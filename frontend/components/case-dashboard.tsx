"use client";

import { RefreshCcw, Microscope, LoaderCircle, ArrowLeft, FileText } from "lucide-react";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import { buildAssetUrl, getCase, startAnalysis } from "@/lib/api";
import { useSession } from "@/lib/use-session";
import type { AnalysisJob, CaseDetail, Evidence } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { SectionCard } from "@/components/section-card";
import { StatusBadge } from "@/components/status-badge";

const ANALYSIS_OPTIONS = [
  { key: "image_forgery", label: "Image Forgery Detection" },
  { key: "document_forgery", label: "Document Forgery Detection" },
  { key: "ai_edited", label: "AI Edited Detection" }
] as const;

export function CaseDashboard() {
  const { session, error: sessionError } = useSession();
  const [caseData, setCaseData] = useState<CaseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [workingLabel, setWorkingLabel] = useState<string | null>(null);

  const refreshCase = async (showSpinner = false) => {
    if (!session) return;
    if (showSpinner) {
      setRefreshing(true);
    }
    try {
      const response = await getCase(session.caseId, session.accessKey);
      setCaseData(response);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load workspace data.");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    if (session) void refreshCase(true);
  }, [session]);

  useEffect(() => {
    if (!caseData?.analysis_jobs.some((job) => job.status === "queued" || job.status === "processing")) {
      return;
    }
    const interval = window.setInterval(() => {
      void refreshCase();
    }, 4000);
    return () => window.clearInterval(interval);
  }, [caseData]);

  const sortedEvidence = useMemo(
    () => [...(caseData?.evidence_items ?? [])].sort((a, b) => new Date(b.uploaded_at).getTime() - new Date(a.uploaded_at).getTime()),
    [caseData]
  );

  const sortedJobs = useMemo(
    () => [...(caseData?.analysis_jobs ?? [])].sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()),
    [caseData]
  );

  const handleAnalysis = async (evidence: Evidence, analysisType: string) => {
    if (!session) return;
    setWorkingLabel(`Starting ${analysisType}`);
    try {
      await startAnalysis(session.caseId, {
        access_key: session.accessKey,
        evidence_id: evidence.id,
        analysis_type: analysisType
      });
      await refreshCase();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to start analysis.");
    } finally {
      setWorkingLabel(null);
    }
  };

  if (sessionError) {
    return <div className="p-10 text-danger text-center">{sessionError}</div>;
  }

  if (loading || !session) {
    return <LoadingShell label="Loading dashboard..." />;
  }

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-6 py-8">
      <div className="mb-8 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.36em] text-accent/80">Case History</p>
          <h1 className="mt-3 text-4xl font-semibold text-white">Log Dashboard</h1>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button variant="ghost" asChild>
             <Link href="/"><ArrowLeft className="mr-2 h-4 w-4"/> Upload Evidence</Link>
          </Button>
          <Button variant="secondary" onClick={() => void refreshCase(true)}>
            <RefreshCcw className="mr-2 h-4 w-4" />
            Sync Status
          </Button>
        </div>
      </div>

      {error ? <div className="mb-6 rounded-xl border border-danger/30 bg-danger/10 p-4 text-sm text-danger">{error}</div> : null}

      <div className="grid gap-6">
        <SectionCard title="Evidence Log" eyebrow="Case History">
          <div className="mb-4 flex items-center gap-3 text-sm">
            <span className="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium bg-success/10 border border-success text-success">Authentic</span>
            <span className="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium bg-warning/10 border border-warning text-warning">Suspicious</span>
            <span className="inline-flex items-center rounded-full px-3 py-1 text-xs font-medium bg-danger/10 border border-danger text-danger">Tampered</span>
            <p className="ml-3 text-xs text-muted">Legend: color indicates the most recent analysis verdict for each evidence.</p>
          </div>

          {sortedEvidence.length === 0 ? (
            <EmptyState label="No evidence uploaded yet." />
          ) : (
            <div className="grid gap-4">
              {sortedEvidence.slice(0, 1).map((evidence) => (
                <EvidenceCard key={evidence.id} evidence={evidence} onAnalyze={handleAnalysis} />
              ))}
            </div>
          )}
        </SectionCard>

        <SectionCard className="mt-6" title="Analysis Queue" eyebrow="Processing">
          {refreshing ? <p className="mb-4 text-xs font-mono uppercase tracking-[0.3em] text-accent/80">Refreshing latest job statuses...</p> : null}
          {sortedJobs.length === 0 ? (
            <EmptyState label="No analyses started yet." />
          ) : (
            <div className="overflow-hidden rounded-2xl border border-border">
              <table className="w-full border-collapse text-left text-sm">
                <thead className="bg-panel/90 text-muted">
                  <tr>
                    <th className="px-4 py-3 font-medium">Job</th>
                    <th className="px-4 py-3 font-medium">Analysis Type</th>
                    <th className="px-4 py-3 font-medium">Status</th>
                    <th className="px-4 py-3 font-medium">Progress</th>
                    <th className="px-4 py-3 font-medium">Report</th>
                  </tr>
                </thead>
                <tbody>
                  {sortedJobs.map((job) => (
                    <JobRow key={job.id} caseId={session.caseId} accessKey={session.accessKey} job={job} />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </SectionCard>
      </div>
    </main>
  );
}

function EvidenceCard({
  evidence,
  onAnalyze
}: {
  evidence: Evidence;
  onAnalyze: (evidence: Evidence, analysisType: string) => Promise<void>;
}) {
  const isImage = evidence.mime_type.startsWith("image/");
  return (
    <article className="grid gap-4 rounded-2xl border border-border bg-panel/70 p-4 lg:grid-cols-[220px_1fr]">
      <div className="overflow-hidden rounded-xl border border-border bg-background/60 h-56 flex items-center justify-center">
        {isImage ? (
          <img
            alt={evidence.original_filename}
            src={buildAssetUrl(evidence.storage_url)}
            className="max-h-full max-w-full object-contain"
            style={{ display: "block" }}
          />
        ) : (
          <div className="flex h-44 items-center justify-center">
            <FileText className="h-12 w-12 text-accent" />
          </div>
        )}
      </div>
      <div>
        <div className="flex flex-wrap items-center gap-3">
          <h3 className="text-lg font-semibold text-text">{evidence.original_filename}</h3>
          <span className="rounded-full border border-border px-3 py-1 font-mono text-xs uppercase tracking-[0.24em] text-muted">{evidence.mime_type}</span>
          {evidence.latest_result ? (
            (() => {
              const status = evidence.latest_result!.forgery_status as string;
              const conf = Math.round(evidence.latest_result!.confidence_score * 100);
              const textMap: Record<string, string> = {
                authentic: `Likely authentic — low probability of forgery (confidence ${conf}%)`,
                suspicious: `Suspicious — possible manipulation detected (confidence ${conf}%)`,
                tampered: `Likely tampered — manipulation detected (confidence ${conf}%)`
              };
              const title = textMap[status] ?? `Status: ${status} (confidence ${conf}%)`;
              const className = {
                authentic: "bg-success/10 border-success text-success",
                suspicious: "bg-warning/10 border-warning text-warning",
                tampered: "bg-danger/10 border-danger text-danger"
              }[status] ?? "bg-panel text-muted";
              return (
                <span title={title} aria-label={title} className={`ml-2 inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${className}`}>
                  {status.replaceAll("_", " ")} • {conf}%
                </span>
              );
            })()
          ) : null}
        </div>
        <div className="mt-3 grid gap-2 text-sm text-muted md:grid-cols-2">
          <p>
            Evidence ID: <span className="font-mono text-text">{evidence.id}</span>
          </p>
          <p>
            Uploaded: <span className="text-text">{formatDate(evidence.uploaded_at)}</span>
          </p>
          <p>
            File Size: <span className="text-text">{formatBytes(evidence.size)}</span>
          </p>
          <p>
            SHA-256: <span className="font-mono text-text">{evidence.file_hash.slice(0, 18)}...</span>
          </p>
        </div>
        <div className="mt-5 flex flex-wrap gap-3">
          {ANALYSIS_OPTIONS.map((option) => (
            <Button key={option.key} variant="secondary" onClick={() => void onAnalyze(evidence, option.key)}>
              <Microscope className="mr-2 h-4 w-4" />
              {option.label}
            </Button>
          ))}
        </div>
        <div className="mt-3">
          {evidence.latest_result?.report?.url ? (
            <a href={evidence.latest_result.report.url} target="_blank" rel="noopener noreferrer">
              <Button variant="ghost">Open Report</Button>
            </a>
          ) : null}
        </div>
      </div>
    </article>
  );
}

function JobRow({ caseId, accessKey, job }: { caseId: string; accessKey: string; job: AnalysisJob }) {
  return (
    <tr className="border-t border-border/80">
      <td className="px-4 py-3 font-mono text-xs text-text">#{job.id}</td>
      <td className="px-4 py-3 text-text">{job.analysis_type.replaceAll("_", " ")}</td>
      <td className="px-4 py-3">
        <StatusBadge value={job.status} />
      </td>
      <td className="px-4 py-3 text-muted">{job.error_text || job.progress_message || "Awaiting update"}</td>
      <td className="px-4 py-3">
        {job.status === "completed" ? (
          <Button asChild variant="ghost">
            <Link href={`/report/${job.id}`}>Open Report</Link>
          </Button>
        ) : (
          <span className="text-xs uppercase tracking-[0.22em] text-muted">Pending</span>
        )}
      </td>
    </tr>
  );
}

function LoadingShell({ label }: { label: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="rounded-2xl border border-border bg-surface/90 p-6 text-center">
        <LoaderCircle className="mx-auto h-8 w-8 animate-spin text-accent" />
        <p className="mt-4 font-mono text-xs uppercase tracking-[0.3em] text-accent/80">{label}</p>
      </div>
    </div>
  );
}

function EmptyState({ label }: { label: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-border bg-panel/40 p-8 text-center text-sm text-muted">
      {label}
    </div>
  );
}

function formatDate(value?: string | null) {
  if (!value) return "Unknown";
  return new Date(value).toLocaleString();
}

function formatBytes(size: number) {
  if (size < 1024) return `${size} B`;
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${(size / (1024 * 1024)).toFixed(2)} MB`;
}
