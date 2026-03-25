export type RecentCase = {
  caseId: string;
  accessKey: string;
  title?: string | null;
  status: string;
  accessedAt: string;
};

const STORAGE_KEY = "forensic_recent_cases";

export function loadRecentCases(): RecentCase[] {
  if (typeof window === "undefined") {
    return [];
  }
  const raw = window.localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return [];
  }
  try {
    return JSON.parse(raw) as RecentCase[];
  } catch {
    return [];
  }
}

export function saveRecentCase(entry: RecentCase) {
  if (typeof window === "undefined") {
    return;
  }
  const next = [entry, ...loadRecentCases().filter((item) => item.caseId !== entry.caseId)].slice(0, 12);
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
}

