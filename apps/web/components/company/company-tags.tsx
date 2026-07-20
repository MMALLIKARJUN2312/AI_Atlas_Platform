import { Badge } from "@/components/ui";

interface CompanyTagsProps {
  tags: string;
}

export function CompanyTags({ tags }: CompanyTagsProps) {
  const items = tags
    .split(",")
    .map((tag) => tag.trim())
    .filter(Boolean);

  return (
    <div className="flex flex-wrap gap-3">
      {items.map((tag) => (
        <Badge key={tag}>{tag}</Badge>
      ))}
    </div>
  );
}
