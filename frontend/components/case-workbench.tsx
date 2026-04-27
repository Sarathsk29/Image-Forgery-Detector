"use client";

import { UploadCloud, LoaderCircle, ArrowRight, Info } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { uploadEvidence } from "@/lib/api";
import { useSession } from "@/lib/use-session";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SectionCard } from "@/components/section-card";

export function CaseWorkbench() {
  const router = useRouter();
  const { session, error: sessionError } = useSession();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [workingLabel, setWorkingLabel] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!selectedFile || !session) {
      setError("Choose an image or PDF evidence file first.");
      return;
    }
    setWorkingLabel("Uploading evidence");
    try {
      await uploadEvidence(session.caseId, session.accessKey, selectedFile);
      setSelectedFile(null);
      router.push("/log");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed.");
    } finally {
      setWorkingLabel(null);
    }
  };

  if (sessionError) {
    return <div className="p-10 text-danger text-center">{sessionError}</div>;
  }

  if (!session) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="rounded-2xl border border-border bg-surface/90 p-6 text-center shadow-xl">
          <LoaderCircle className="mx-auto h-8 w-8 animate-spin text-accent" />
          <p className="mt-4 font-mono text-xs uppercase tracking-[0.3em] text-accent/80">Initializing workspace...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-6 py-8">
      <div className="mb-8 flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.36em] text-accent/80">Active Assessment</p>
          <div className="mt-3 flex items-start gap-4">
            <h1 className="max-w-4xl text-2xl font-semibold leading-relaxed text-white lg:text-3xl">
              Copy-Move Image Forgery Detection Using SIFT Algorithm with Tampered Region Localization for Digital Image Authentication (Hybrid)
            </h1>
            <div className="group relative z-50 flex cursor-help items-center mt-2">
              <Info className="h-6 w-6 text-muted transition-colors hover:text-accent" />
              <div className="pointer-events-none absolute left-full top-1/2 ml-3 w-80 -translate-y-1/2 translate-x-2 opacity-0 transition-all group-hover:translate-x-0 group-hover:opacity-100">
                <div className="rounded-xl border border-border bg-panel p-5 text-xs font-medium text-muted/80 shadow-2xl">
                  <p className="mb-2 text-sm font-semibold tracking-wide text-text">MCA Project: ForensIQ</p>
                  <p className="mb-3 leading-relaxed">This platform is an advanced digital forensic tool designed to detect image and document tampering using AI models.</p>
                  <p className="mb-1 text-text">Workflow:</p>
                  <ol className="list-decimal space-y-1.5 pl-4 leading-relaxed">
                    <li>Start by uploading a suspicious document or image.</li>
                    <li>Select an AI engine to analyze for latent manipulation markers.</li>
                    <li>Review the generated digital forensic intelligence report.</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-muted">
            <span>Session initiated automatically</span>
          </div>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button variant="secondary" asChild>
            <Link href="/log">View Dashboard <ArrowRight className="ml-2 h-4 w-4" /></Link>
          </Button>
        </div>
      </div>

      {error ? <div className="mb-6 rounded-xl border border-danger/30 bg-danger/10 p-4 text-sm text-danger">{error}</div> : null}

      <div className="mx-auto mt-12 max-w-lg">
        <SectionCard title="Submit Evidence" eyebrow="Upload">
          <div
            className="rounded-2xl border border-dashed border-border bg-panel/60 p-8 text-center transition-colors focus-within:border-accent hover:border-accent/40"
            onDrop={(event) => {
              event.preventDefault();
              setSelectedFile(event.dataTransfer.files?.[0] ?? null);
            }}
            onDragOver={(event) => event.preventDefault()}
          >
            <UploadCloud className="mx-auto h-12 w-12 text-accent opacity-80" />
            <p className="mt-4 text-lg font-semibold text-text">Drag and drop an image or PDF</p>
            <p className="mt-2 text-sm text-muted/80">Maximum upload size: 5 MB. Supported formats: JPG, PNG, WEBP, BMP, TIFF, PDF.</p>
            <Input
              className="mt-6 cursor-pointer bg-background"
              type="file"
              accept=".jpg,.jpeg,.png,.webp,.bmp,.tiff,.pdf"
              onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
            />
            {selectedFile ? <p className="mt-4 font-mono text-xs font-medium text-accent">Selected file: {selectedFile.name}</p> : null}
            <Button className="mt-6 w-full py-5 text-base tracking-wide" disabled={!selectedFile || Boolean(workingLabel)} onClick={handleUpload}>
              {workingLabel === "Uploading evidence" ? "Uploading..." : "Submit Evidence"}
            </Button>
          </div>
        </SectionCard>
      </div>
    </main>
  );
}
