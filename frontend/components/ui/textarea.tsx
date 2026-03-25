import * as React from "react";

import { cn } from "@/lib/utils";

export const Textarea = React.forwardRef<HTMLTextAreaElement, React.TextareaHTMLAttributes<HTMLTextAreaElement>>(
  ({ className, ...props }, ref) => (
    <textarea
      ref={ref}
      className={cn(
        "min-h-28 w-full rounded-md border border-border bg-surface px-3 py-3 text-sm text-text outline-none transition placeholder:text-muted focus:border-accent",
        className
      )}
      {...props}
    />
  )
);

Textarea.displayName = "Textarea";
