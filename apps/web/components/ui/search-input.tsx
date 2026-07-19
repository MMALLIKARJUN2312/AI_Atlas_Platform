import { forwardRef } from "react";
import { Search } from "lucide-react";

import { cn } from "@/lib/utils";
import { Input, InputProps } from "./input";

export interface SearchInputProps extends InputProps {
  containerClassName?: string;
}

export const SearchInput = forwardRef<
  HTMLInputElement,
  SearchInputProps
>(({ className, containerClassName, ...props }, ref) => {
  return (
    <div
      className={cn(
        "relative flex items-center",
        containerClassName
      )}
    >
      <Search
        className="pointer-events-none absolute left-4 h-5 w-5 text-zinc-500"
        aria-hidden="true"
      />

      <Input
        ref={ref}
        type="search"
        className={cn("pl-12", className)}
        {...props}
      />
    </div>
  );
});

SearchInput.displayName = "SearchInput";