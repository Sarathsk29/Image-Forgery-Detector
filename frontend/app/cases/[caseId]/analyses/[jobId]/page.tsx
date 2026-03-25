import { ReportView } from "@/components/report-view";

export default function AnalysisReportPage({
  params,
  searchParams
}: {
  params: { caseId: string; jobId: string };
  searchParams: { accessKey?: string };
}) {
  return <ReportView caseId={params.caseId} jobId={params.jobId} accessKey={searchParams.accessKey ?? ""} />;
}
