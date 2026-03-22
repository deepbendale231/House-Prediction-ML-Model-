export default function HistoryLoading() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 md:px-8">
      <div className="mb-8 h-10 w-64 animate-pulse rounded-lg bg-slate-800/80" />
      <div className="surface-card p-4">
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, idx) => (
            <div key={idx} className="h-12 animate-pulse rounded-lg bg-slate-800/80" />
          ))}
        </div>
      </div>
    </div>
  );
}
