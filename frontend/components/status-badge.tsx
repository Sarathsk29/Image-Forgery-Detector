import React from "react";
import { cn } from "@/lib/utils";

const toneMap: Record<string, string> = {
  open: "border-accent/40 bg-accent/10 text-accent",
  queued: "border-warning/40 bg-warning/10 text-warning",
  processing: "border-warning/40 bg-warning/10 text-warning",
  completed: "border-success/40 bg-success/10 text-success",
  authentic: "border-success/40 bg-success/10 text-success",
  suspicious: "border-warning/40 bg-warning/10 text-warning",
  tampered: "border-danger/40 bg-danger/10 text-danger",
  failed: "border-danger/40 bg-danger/10 text-danger"
};

export function StatusBadge({ value }: { value: string }) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full border px-3 py-1 font-mono text-xs uppercase tracking-[0.22em]",
        toneMap[value] ?? "border-border bg-panel text-muted"
      )}
    >
      {value.replaceAll("_", " ")}
    </span>
  );
}

