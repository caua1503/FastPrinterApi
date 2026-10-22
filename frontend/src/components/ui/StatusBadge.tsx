import React from "react";
import type { PrinterStatus } from "../../types";
import { statusLabel, statusColors } from "../../data/mockData";
import { cn } from "../../lib/utils";

interface StatusBadgeProps {
  status: PrinterStatus;
  className?: string;
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = statusColors[status] || statusColors.excelente;
  const label = statusLabel[status] || status;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold",
        config.bg,
        config.text,
        className
      )}
    >
      <span className={cn("w-1.5 h-1.5 rounded-full", config.dot)} />
      {label}
    </span>
  );
}

export function StatusDot({ status, className }: StatusBadgeProps) {
  const config = statusColors[status] || statusColors.excelente;
  const label = statusLabel[status] || status;

  return (
    <span className={cn("inline-flex items-center gap-1.5 font-semibold text-xs", config.text, className)}>
      <span className={cn("w-2 h-2 rounded-full shrink-0", config.dot)} />
      {label}
    </span>
  );
}
