"use client";

import { Download, LoaderCircle, ShieldAlert, ShieldCheck, TriangleAlert } from "lucide-react";
import { useEffect, useState } from "react";

import { buildAssetUrl, getAnalysisJob, getAnalysisReport, getAnalysisResult } from "@/lib/api";
import type { AnalysisJob, AnalysisResult, Report } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { SectionCard } from "@/components/section-card";
import { StatusBadge } from "@/components/status-badge";


export function ReportView({ caseId, jobId, accessKey }: { caseId: string; jobId: string; accessKey: string }) {
  const [job, setJob] = useState<AnalysisJob | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    const load = async () => {
      try {
        const jobResponse = await getAnalysisJob(jobId, accessKey);
        if (cancelled) return;
        setJob(jobResponse);
        if (jobResponse.status === "completed") {
          const [resultResponse, reportResponse] = await Promise.all([
            getAnalysisResult(jobId, accessKey),
            getAnalysisReport(jobId, accessKey)
          ]);
          if (cancelled) return;
          setResult(resultResponse);
          setReport(reportResponse);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Unable to load analysis report.");
        }
      }
    };

    void load();
    const interval = window.setInterval(() => {
      void load();
    }, 4000);

    return () => {
      cancelled = true;
      window.clearInterval(interval);
    };
  }, [jobId, accessKey]);

  if (error) {
    return <CenteredMessage title="Unable to load analysis report" subtitle={error} />;
  }

  if (!job) {
    return <CenteredLoader label="Loading analysis job" />;
  }

  if (job.status !== "completed" || !result || !report) {
    return <CenteredLoader label={job.progress_message || "Analysis is still running"} />;
  }

  const confidencePercent = `${Math.round(result.confidence_score * 100)}%`;
  const icon =
    result.forgery_status === "tampered" ? (
      <ShieldAlert className="h-6 w-6 text-danger" />
    ) : result.forgery_status === "suspicious" ? (
      <TriangleAlert className="h-6 w-6 text-warning" />
    ) : (
      <ShieldCheck className="h-6 w-6 text-success" />
    );

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-6 py-8">
      <div className="mb-8 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.36em] text-accent/80">Analysis Report</p>
          <h1 className="mt-3 text-4xl font-semibold text-white">Forensic Report for Job #{job.id}</h1>
          <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-muted">
            <span>Case ID: <span className="font-mono text-text">{caseId}</span></span>
            <StatusBadge value={result.forgery_status} />
            <span>Analysis Type: <span className="text-text">{job.analysis_type.replaceAll("_", " ")}</span></span>
          </div>
        </div>
        <Button asChild>
          <a href={buildAssetUrl(report.url)} target="_blank" rel="noreferrer">
            <Download className="mr-2 h-4 w-4" />
            Download PDF Report
          </a>
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <MetricCard label="Forgery Status" value={result.forgery_status.replaceAll("_", " ")} icon={icon} />
        <MetricCard label="Confidence Score" value={confidencePercent} />
        <MetricCard label="Methods Used" value={String(result.methods.length)} helper={result.methods.join(", ")} />
      </div>

      <div className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <SectionCard title="Investigation Summary" eyebrow="Overview">
          <p className="text-sm leading-7 text-muted">{result.summary}</p>
          <div className="mt-5 flex flex-wrap gap-2">
            {result.methods.map((method) => (
              <span key={method} className="rounded-full border border-border px-3 py-1 text-xs uppercase tracking-[0.22em] text-muted">
                {method}
              </span>
            ))}
          </div>
          <div className="mt-6 rounded-2xl border border-border bg-panel/60 p-4">
            <h3 className="text-sm font-semibold text-text">Final Conclusion</h3>
            <p className="mt-2 text-sm leading-7 text-muted">{String(result.findings.conclusion ?? "Conclusion not available.")}</p>
          </div>
        </SectionCard>

        <SectionCard title="Structured Findings" eyebrow="Evidence">
          <dl className="grid gap-3">
            {Object.entries(result.findings)
              .filter(([key]) => !["artifact_manifest", "conclusion", "regions", "page_findings", "suspicious_boxes"].includes(key))
              .map(([key, value]) => {
                const isArray = Array.isArray(value);
                const isObject = value !== null && typeof value === "object" && !isArray;
                const isEmptyArray = isArray && value.length === 0;

                return (
                  <div key={key} className="rounded-xl border border-border bg-panel/50 p-4">
                    <dt className="font-mono text-xs uppercase tracking-[0.25em] text-accent/80 mb-2">
                      {key.replaceAll("_", " ")}
                    </dt>
                    <dd className="text-sm leading-6 text-muted">
                      {typeof value === "string" ? (
                        <p>{value}</p>
                      ) : isEmptyArray ? (
                        <p className="text-muted/50 italic">None found</p>
                      ) : isArray ? (
                        <ul className="list-disc list-inside space-y-1">
                          {value.map((item: any, i: number) => (
                            <li key={i} className="text-text">{String(item)}</li>
                          ))}
                        </ul>
                      ) : isObject ? (
                        <div className="mt-2 grid grid-cols-1 gap-x-4 gap-y-3 sm:grid-cols-2">
                          {Object.entries(value).map(([subKey, subVal]) => (
                            <div key={subKey} className="flex flex-col border-b border-border/40 pb-1">
                              <span className="text-[11px] uppercase tracking-wider text-muted/70">{subKey.replaceAll("_", " ")}</span>
                              <span className="mt-0.5 truncate font-medium text-text" title={String(subVal)}>
                                {subVal !== null && subVal !== "" ? String(subVal) : <span className="text-muted/40 italic">empty</span>}
                              </span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p>{String(value)}</p>
                      )}
                    </dd>
                  </div>
                );
              })}
          </dl>
        </SectionCard>
      </div>

      <SectionCard className="mt-6" title="Visual Evidence" eyebrow="Artifacts">
        {result.artifacts.length === 0 ? (
          <p className="text-sm text-muted">No visual artifacts were generated for this analysis.</p>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
            {result.artifacts.map((artifact) => (
              <div key={artifact.url} className="overflow-hidden rounded-2xl border border-border bg-panel/50">
                <img alt={artifact.label} className="h-56 w-full object-cover" src={buildAssetUrl(artifact.url)} />
                <div className="border-t border-border p-4">
                  <p className="text-sm font-medium text-text">{artifact.label}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </SectionCard>

      <div className="mt-6 grid gap-6 xl:grid-cols-2">
        {"regions" in result.findings && (result.findings.regions as any[]).length > 0 ? (
          <SectionCard title="Identified Copy-Move Clones" eyebrow="Spatial Clues">
             <div className="grid gap-3">
              {(result.findings.regions as any[]).map((region, idx) => (
                <div key={idx} className="flex flex-col gap-1 rounded-xl border border-border bg-panel/50 p-4 text-sm leading-6 text-muted">
                  <p>
                    <span className="font-semibold text-accent">Match Pair #{idx + 1}:</span> A nearly identical image patch was duplicated.
                  </p>
                  <div className="flex flex-wrap items-center text-xs font-mono gap-3 mt-1 bg-background p-2 px-3 rounded border border-border">
                    <span>Source: ({region.from?.x ?? "N/A"}, {region.from?.y ?? "N/A"})</span>
                    <span className="text-muted">→</span>
                    <span>Clone: ({region.to?.x ?? "N/A"}, {region.to?.y ?? "N/A"})</span>
                    <span className="ml-auto text-warning font-semibold">Dist: {region.distance}px</span>
                  </div>
                </div>
              ))}
            </div>
          </SectionCard>
        ) : null}
        {"page_findings" in result.findings ? (
          <SectionCard title="Page Analysis" eyebrow="Document Review">
            <div className="grid gap-4">
              {(result.findings.page_findings as any[]).map((pf, idx) => {
                const elaPerc = Math.round((pf.ela_score || 0) * 100);
                const lcrPerc = Math.round((pf.low_confidence_ratio || 0) * 100);
                const curScorePerc = Math.round((pf.page_score || 0) * 100);
                const boxesCnt = pf.suspicious_boxes ? pf.suspicious_boxes.length : 0;
                
                return (
                  <div key={idx} className="rounded-xl border border-border bg-panel/50 p-4">
                    <h4 className="text-sm font-semibold text-text mb-3">Page {pf.page || idx + 1} Overview (Anomaly Score: {curScorePerc}%)</h4>
                    <ul className="list-disc list-inside text-sm leading-6 text-muted space-y-1">
                      <li>Error Level Analysis (ELA) indicated a {elaPerc}% probability of anomalous regions.</li>
                      {pf.font_outlier_ratio !== undefined && (
                        <li>Font variance analysis detected {Math.round(pf.font_outlier_ratio * 100)}% of text elements with outlier font sizes.</li>
                      )}
                      <li>OCR confidence was unusually low for {lcrPerc}% of the detected text.</li>
                      {boxesCnt > 0 && (
                        <li>
                          Located {boxesCnt} specific bounding box(es) with suspicious or severely degraded text confidence:
                          <div className="mt-2 flex flex-wrap gap-2">
                            {pf.suspicious_boxes.map((box: any, bIdx: number) => (
                              <span key={bIdx} className="rounded border border-border bg-background px-2 py-1 text-xs">
                                <span className="font-mono text-accent">"{box.text?.trim() || "<empty>"}"</span> <span className="text-muted ml-1">(Conf: {box.confidence}%)</span>
                              </span>
                            ))}
                          </div>
                        </li>
                      )}
                      <li className="mt-2 list-none">
                        {curScorePerc >= 40 ? (
                          <span className="text-warning">⚠️ Overall, this page shows significant signs of potential tampering or heavy degradation.</span>
                        ) : (
                          <span className="text-success">✓ This page appears largely consistent with no dominant red flags.</span>
                        )}
                      </li>
                    </ul>
                  </div>
                );
              })}
            </div>
          </SectionCard>
        ) : null}
      </div>
    </main>
  );
}

function MetricCard({
  label,
  value,
  helper,
  icon
}: {
  label: string;
  value: string;
  helper?: string;
  icon?: React.ReactNode;
}) {
  return (
    <div className="rounded-2xl border border-border bg-surface/90 p-5 shadow-panel">
      <div className="flex items-center justify-between gap-3">
        <p className="font-mono text-xs uppercase tracking-[0.3em] text-accent/80">{label}</p>
        {icon}
      </div>
      <p className="mt-4 text-3xl font-semibold text-white">{value}</p>
      {helper ? <p className="mt-2 text-sm leading-6 text-muted">{helper}</p> : null}
    </div>
  );
}

function CenteredLoader({ label }: { label: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="rounded-2xl border border-border bg-surface/90 p-6 text-center">
        <LoaderCircle className="mx-auto h-8 w-8 animate-spin text-accent" />
        <p className="mt-4 font-mono text-xs uppercase tracking-[0.3em] text-accent/80">{label}</p>
      </div>
    </div>
  );
}

function CenteredMessage({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="max-w-xl rounded-2xl border border-danger/20 bg-surface/90 p-6 text-center">
        <h1 className="text-2xl font-semibold text-white">{title}</h1>
        <p className="mt-3 text-sm leading-7 text-muted">{subtitle}</p>
      </div>
    </div>
  );
}

