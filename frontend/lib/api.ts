import type {
  AnalysisJob,
  AnalysisResult,
  CaseDetail,
  CreateCaseResponse,
  Report
} from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

type RequestOptions = RequestInit & {
  rawBody?: BodyInit | null;
};

export async function apiRequest<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { rawBody, headers, ...rest } = options;
  const response = await fetch(`${API_BASE}${path}`, {
    ...rest,
    headers: {
      ...(rawBody instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...headers
    },
    body: rawBody ?? rest.body
  });

  if (!response.ok) {
    const fallback = await response.text();
    let detail = fallback;
    try {
      const parsed = JSON.parse(fallback);
      detail = parsed.detail ?? fallback;
    } catch {
      detail = fallback;
    }
    throw new Error(detail || "Request failed");
  }

  return response.json() as Promise<T>;
}

export const buildAssetUrl = (url: string) => (url.startsWith("http") ? url : `${API_BASE}${url}`);

export const createCase = (payload: { title?: string; notes?: string }) =>
  apiRequest<CreateCaseResponse>("/api/cases", {
    method: "POST",
    body: JSON.stringify(payload)
  });

export const openCase = (payload: { case_id: string; access_key: string }) =>
  apiRequest<CaseDetail>("/api/cases/open", {
    method: "POST",
    body: JSON.stringify(payload)
  });

export const getCase = (caseId: string, accessKey: string) =>
  apiRequest<CaseDetail>(`/api/cases/${caseId}?access_key=${encodeURIComponent(accessKey)}`);

export const uploadEvidence = (caseId: string, accessKey: string, file: File) => {
  const formData = new FormData();
  formData.append("access_key", accessKey);
  formData.append("file", file);
  return apiRequest(`/api/cases/${caseId}/evidence`, {
    method: "POST",
    rawBody: formData
  });
};

export const startAnalysis = (caseId: string, payload: { access_key: string; evidence_id: number; analysis_type: string }) =>
  apiRequest<AnalysisJob>(`/api/cases/${caseId}/analyses`, {
    method: "POST",
    body: JSON.stringify(payload)
  });

export const getAnalysisJob = (jobId: number | string, accessKey: string) =>
  apiRequest<AnalysisJob>(`/api/analyses/${jobId}?access_key=${encodeURIComponent(accessKey)}`);

export const getAnalysisResult = (jobId: number | string, accessKey: string) =>
  apiRequest<AnalysisResult>(`/api/analyses/${jobId}/result?access_key=${encodeURIComponent(accessKey)}`);

export const getAnalysisReport = (jobId: number | string, accessKey: string) =>
  apiRequest<Report>(`/api/analyses/${jobId}/report?access_key=${encodeURIComponent(accessKey)}`);

