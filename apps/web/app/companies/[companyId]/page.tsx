import { CompanyDetailPage } from "@/features/company";

interface CompanyPageProps {
  params: Promise<{
    companyId: string;
  }>;
}

export default function CompanyPage(
  props: CompanyPageProps
) {
  return (
    <CompanyDetailPage
      params={props.params}
    />
  );
}