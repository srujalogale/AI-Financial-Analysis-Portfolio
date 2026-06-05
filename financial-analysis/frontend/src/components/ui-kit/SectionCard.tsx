import { ReactNode } from "react";

interface SectionCardProps {
  title?: string;
  description?: string;
  children: ReactNode;
  action?: ReactNode;
  className?: string;
  contentClassName?: string;
}

export function SectionCard({
  title,
  description,
  children,
  action,
  className = "",
  contentClassName = "",
}: SectionCardProps) {
  return (
    <div
      className={`rounded-xl border border-border bg-background p-6 ${className}`}
    >
      {(title || description || action) && (
        <div className="mb-4 flex items-start justify-between">
          <div>
            {title && (
              <h2 className="text-xl font-semibold">
                {title}
              </h2>
            )}

            {description && (
              <p className="text-sm text-muted-foreground">
                {description}
              </p>
            )}
          </div>

          {action && <div>{action}</div>}
        </div>
      )}

      <div className={contentClassName}>
        {children}
      </div>
    </div>
  );
}