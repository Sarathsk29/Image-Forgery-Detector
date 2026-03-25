export type Evidence = {
  id: number;
  original_filename: string;
  mime_type: string;
  size: number;
  storage_url: string;
  file_hash: string;
  uploaded_at: string;
};

export type AnalysisJob = {
  id: number;
  evidence_id: number;
  analysis_type: "image_forgery" | "document_forgery" | "ai_edited";
  status: "queued" | "processing" | "completed" | "failed";
  progress_message?: string | null;
  error_text?: string | null;
  created_at: string;
  started_at?: string | null;
  completed_at?: string | null;
};

export type Artifact = {
  label: string;
  url: string;
};

export type AnalysisResult = {
  forgery_status: "authentic" | "suspicious" | "tampered";
  confidence_score: number;
  summary: string;
  methods: string[];
  findings: Record<string, unknown>;
  artifacts: Artifact[];
};

export type Report = {
  url: string;
  generated_at: string;
};

export type CaseDetail = {
  case_id: string;
  title?: string | null;
  notes?: string | null;
  status: string;
  created_at: string;
  evidence_items: Evidence[];
  analysis_jobs: AnalysisJob[];
};

export type CreateCaseResponse = {
  case_id: string;
  access_key: string;
  status: string;
  created_at: string;
};

