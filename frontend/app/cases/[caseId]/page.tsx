import { CaseWorkbench } from "@/components/case-workbench";

export default function CasePage({
  params,
  searchParams
}: {
  params: { caseId: string };
  searchParams: { accessKey?: string };
}) {
  return <CaseWorkbench caseId={params.caseId} accessKey={searchParams.accessKey ?? ""} />;
}

