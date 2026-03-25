"use client";
import React from "react";

import { ShieldCheck, FileScan, ScanSearch, FolderOpenDot } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";

import { createCase, openCase } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { SectionCard } from "@/components/section-card";


export function LandingShell() {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);
  const [created, setCreated] = useState<{ caseId: string; accessKey: string } | null>(null);
  const [createForm, setCreateForm] = useState({ title: "", notes: "" });
  const [openForm, setOpenForm] = useState({ caseId: "", accessKey: "" });

  const handleCreate = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      const response = await createCase({ title: createForm.title, notes: createForm.notes });
      setCreated({ caseId: response.case_id, accessKey: response.access_key });
      startTransition(() => {
        router.push(`/cases/${response.case_id}?accessKey=${encodeURIComponent(response.access_key)}`);
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to create case.");
    }
  };

  const handleOpen = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    try {
      await openCase({ case_id: openForm.caseId, access_key: openForm.accessKey });
      startTransition(() => {
        router.push(`/cases/${openForm.caseId}?accessKey=${encodeURIComponent(openForm.accessKey)}`);
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to open case.");
    }
  };

  return (
    <main className="relative mx-auto min-h-screen max-w-7xl px-6 py-10">
      <div className="mb-10 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div className="max-w-3xl">
          <p className="font-mono text-xs uppercase tracking-[0.36em] text-accent/80">Forensic Investigation Platform</p>
          <h1 className="mt-4 text-4xl font-semibold leading-tight text-white md:text-6xl">
            Multi-Modal Digital Forgery Detection for Images and Documents
          </h1>
          <p className="mt-4 max-w-2xl text-base leading-7 text-muted">
            Create a case, submit evidence, run hybrid forensic analysis, and export structured reports with localized visual proof.
          </p>
        </div>
        <div className="grid gap-3 rounded-2xl border border-border bg-surface/80 p-4 backdrop-blur">
          <div className="flex items-center gap-3">
            <ShieldCheck className="h-5 w-5 text-accent" />
            <span className="text-sm text-text">Case ID + access key workflow</span>
          </div>
          <div className="flex items-center gap-3">
            <FileScan className="h-5 w-5 text-accent" />
            <span className="text-sm text-text">SIFT, ELA, OCR, metadata, artifact analysis</span>
          </div>
          <div className="flex items-center gap-3">
            <ScanSearch className="h-5 w-5 text-accent" />
            <span className="text-sm text-text">Evidence localization and downloadable PDF reports</span>
          </div>
        </div>
      </div>

      {error ? <div className="mb-6 rounded-xl border border-danger/30 bg-danger/10 p-4 text-sm text-danger">{error}</div> : null}
      {created ? (
        <div className="mb-6 rounded-xl border border-success/30 bg-success/10 p-4 text-sm text-success">
          Case created. Save this access key before sharing the case: <span className="font-mono">{created.accessKey}</span>
        </div>
      ) : null}

      <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
        <SectionCard title="Create New Case" eyebrow="Intake">
          <form className="space-y-4" onSubmit={handleCreate}>
            <div className="space-y-2">
              <label className="text-sm text-muted">Case Title</label>
              <Input
                value={createForm.title}
                onChange={(event) => setCreateForm((current) => ({ ...current, title: event.target.value }))}
                placeholder="Example: Suspicious property deed image set"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm text-muted">Investigation Notes</label>
              <Textarea
                value={createForm.notes}
                onChange={(event) => setCreateForm((current) => ({ ...current, notes: event.target.value }))}
                placeholder="Describe what makes this evidence suspicious and what you want to verify."
              />
            </div>
            <Button disabled={isPending} type="submit">
              Create Case
            </Button>
          </form>
        </SectionCard>

        <div className="space-y-6">
          <SectionCard title="Open Existing Case" eyebrow="Reopen">
            <form className="space-y-4" onSubmit={handleOpen}>
              <div className="space-y-2">
                <label className="text-sm text-muted">Case ID</label>
                <Input
                  value={openForm.caseId}
                  onChange={(event) => setOpenForm((current) => ({ ...current, caseId: event.target.value.toUpperCase() }))}
                  placeholder="CASE-20260325-AB12CD"
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm text-muted">Access Key</label>
                <Input
                  value={openForm.accessKey}
                  onChange={(event) => setOpenForm((current) => ({ ...current, accessKey: event.target.value.toUpperCase() }))}
                  placeholder="AB12-CD34-EF56"
                />
              </div>
              <Button disabled={isPending} type="submit" variant="secondary">
                <FolderOpenDot className="mr-2 h-4 w-4" />
                Open Case
              </Button>
            </form>
          </SectionCard>

          <SectionCard title="Available Analysis Types" eyebrow="Methods">
            <div className="grid gap-3">
              <MethodItem title="Image Forgery Detection" description="Copy-move detection with local feature matching, spatial filtering, RANSAC, and ELA overlays." />
              <MethodItem title="Document Forgery Detection" description="Metadata review, OCR confidence hotspots, formatting anomaly checks, and page-level ELA." />
              <MethodItem title="AI Edited Detection" description="Heuristic artifact analysis for synthetic edits, hidden post-processing, edge irregularity, and residual noise maps." />
            </div>
          </SectionCard>
        </div>
      </div>
    </main>
  );
}

function MethodItem({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded-xl border border-border bg-panel/70 p-4">
      <h3 className="text-sm font-semibold text-text">{title}</h3>
      <p className="mt-2 text-sm leading-6 text-muted">{description}</p>
    </div>
  );
}

