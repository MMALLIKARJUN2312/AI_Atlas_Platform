import { ReactNode } from "react";

type Props = {
  children: ReactNode;
};

export function PageContainer({
  children,
}: Props) {
  return (
    <main className="min-h-screen p-8">
      {children}
    </main>
  );
}