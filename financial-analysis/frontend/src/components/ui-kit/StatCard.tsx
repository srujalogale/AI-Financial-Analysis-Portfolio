interface StatCardProps {
  label?: string;
  value?: string;
  change?: number;
  hint?: string;
}

export function StatCard({
  label,
  value,
  change,
  hint,
}: StatCardProps) {
  return (
    <div className="rounded-xl border p-4">
      <p>{label}</p>
      <h2>{value}</h2>

      {change !== undefined && (
        <p>{change}%</p>
      )}

      {hint && <p>{hint}</p>}
    </div>
  );
}