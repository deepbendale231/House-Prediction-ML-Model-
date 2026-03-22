"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { History, ArrowLeft, ArrowRight } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { ApiError, PredictionRecord, getPredictionHistory } from "@/lib/api";

const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

function formatDate(value: string) {
  return new Date(value).toLocaleString("en-US", {
    month: "short",
    day: "2-digit",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).replace(",", " ·");
}

const PAGE_SIZE = 10;

export default function HistoryPage() {
  const [rows, setRows] = useState<PredictionRecord[]>([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const offset = (page - 1) * PAGE_SIZE;

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getPredictionHistory(PAGE_SIZE + 1, offset);
        setRows(data);
      } catch (err) {
        if (err instanceof ApiError) setError(`${err.message} (HTTP ${err.status})`);
        else setError("Failed to load prediction history.");
      } finally {
        setLoading(false);
      }
    };

    void run();
  }, [offset]);

  const hasNext = rows.length > PAGE_SIZE;
  const visibleRows = useMemo(() => rows.slice(0, PAGE_SIZE), [rows]);
  const pageCount = hasNext ? page + 1 : page;

  return (
    <div className="mx-auto w-full max-w-6xl px-4 md:px-8">
      <div className="mb-8 flex items-center gap-3">
        <h1 className="text-3xl font-extrabold md:text-[36px]">Prediction History</h1>
        <span className="rounded-full border border-slate-600 bg-slate-800 px-3 py-1 text-xs text-slate-300">
          {visibleRows.length}
        </span>
      </div>

      {loading ? (
        <div className="surface-card overflow-hidden p-4">
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, idx) => (
              <div key={idx} className="h-12 animate-pulse rounded-lg bg-slate-800/80" />
            ))}
          </div>
        </div>
      ) : error ? (
        <div className="surface-card p-5 text-rose-400">{error}</div>
      ) : visibleRows.length === 0 ? (
        <div className="surface-card grid place-items-center gap-3 p-14 text-center">
          <History className="h-8 w-8 text-[var(--color-muted)]" />
          <p className="text-[var(--color-muted)]">No predictions yet. Make your first one.</p>
          <Link href="/" className="text-sm text-sky-300 underline underline-offset-4">
            Go to prediction form
          </Link>
        </div>
      ) : (
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="surface-card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full text-left text-sm">
              <thead className="bg-slate-900/60 text-[var(--color-muted)]">
                <tr>
                  <th className="px-4 py-3">Date</th>
                  <th className="px-4 py-3">Predicted Price</th>
                  <th className="px-4 py-3">Ocean Proximity</th>
                  <th className="px-4 py-3">Median Income</th>
                  <th className="px-4 py-3">Housing Age</th>
                  <th className="px-4 py-3">Actions</th>
                </tr>
              </thead>
              <tbody>
                {visibleRows.map((row) => (
                  <tr key={row.prediction_id} className="border-t border-[var(--color-border)] transition hover:bg-sky-400/5">
                    <td className="px-4 py-3">{formatDate(row.created_at)}</td>
                    <td className="px-4 py-3 font-semibold text-sky-300">{money.format(row.predicted_price)}</td>
                    <td className="px-4 py-3">{row.ocean_proximity}</td>
                    <td className="px-4 py-3">{row.median_income.toFixed(2)}</td>
                    <td className="px-4 py-3">{row.housing_median_age}</td>
                    <td className="px-4 py-3 text-xs text-[var(--color-muted)]">{row.prediction_id.slice(0, 8)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex items-center justify-between border-t border-[var(--color-border)] px-4 py-3">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page === 1}
              className="inline-flex items-center gap-2 rounded-lg border border-[var(--color-border)] px-3 py-2 text-sm disabled:opacity-40"
            >
              <ArrowLeft className="h-4 w-4" /> Previous
            </button>
            <span className="text-sm text-[var(--color-muted)]">Page {page} of {pageCount}</span>
            <button
              onClick={() => hasNext && setPage((p) => p + 1)}
              disabled={!hasNext}
              className="inline-flex items-center gap-2 rounded-lg border border-[var(--color-border)] px-3 py-2 text-sm disabled:opacity-40"
            >
              Next <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}
