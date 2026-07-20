import { Search } from "lucide-react";

import { Input } from "./input";

export function SearchInput(
  props: React.InputHTMLAttributes<HTMLInputElement>
) {
  return (
    <div className="relative">
      <Search
        size={20}
        className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-500"
      />

      <Input
        className="pl-14"
        {...props}
      />
    </div>
  );
}