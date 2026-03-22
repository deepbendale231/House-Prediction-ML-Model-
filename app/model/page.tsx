"use client";

import { motion } from "framer-motion";
import { Activity, Gauge, Medal, Sigma } from "lucide-react";
import { useEffect, useState } from "react";

import { ApiError, ModelInfo, getModelInfo } from "@/lib/api";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 18 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.35, ease: [0.16, 1, 0.3, 1] as const },
  },
};

function formatDate(value: string) {
  return new Date(value).toLocaleString("en-US", {
    month: "short",
    day: "2-digit",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

export default function ModelPage() {
  const [data, setData] = useState<ModelInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await getModelInfo();
        setData(res);
      } catch (err) {
        if (err instanceof ApiError) setError(`${err.message} (HTTP ${err.status})`);
        else setError("Failed to load model info.");
      } finally {
        setLoading(false);
      }
    };

    void run();
  }, []);

  return (
    <div className="mx-auto w-full max-w-6xl px-4 md:px-8">
      <h1 className="mb-8 text-3xl font-extrabold md:text-[36px]">Model Intelligence</h1>

      {loading ? (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="surface-card h-28 animate-pulse bg-slate-900/70" />
          ))}
        </div>
      ) : error || !data ? (
        <div className="surface-card p-5 text-rose-400">{error ?? "No model metadata available."}</div>
      ) : (
        <motion.div variants={container} initial="hidden" animate="show" className="space-y-6">
          <motion.section variants={item} className="grid grid-cols-1 gap-4 md:grid-cols-4">
            {[
              {
                label: "Version",
                value: data.version,
                icon: Medal,
                color: "text-sky-300",
              },
              {
                label: "RMSE",
                value: Number(data.rmse).toFixed(4),
                icon: Activity,
                color: "text-orange-400",
              },
              {
                label: "MAE",
                value: Number(data.mae).toFixed(4),
                icon: Gauge,
                color: "text-yellow-300",
              },
              {
                label: "R²",
                value: Number(data.r2).toFixed(4),
                icon: Sigma,
                color: "text-emerald-400",
              },
            ].map((stat) => {
              const Icon = stat.icon;
              return (
                <article key={stat.label} className="surface-card p-5">
                  <div className="mb-3 flex items-center justify-between">
                    <span className="text-sm text-[var(--color-muted)]">{stat.label}</span>
                    <Icon className={`h-4 w-4 ${stat.color}`} />
                  </div>
                  <div className="text-2xl font-bold">{stat.value}</div>
                </article>
              );
            })}
          </motion.section>

          <motion.section variants={item} className="surface-card p-5">
            <h2 className="mb-2 text-lg font-semibold">Trained At</h2>
            <p className="text-[var(--color-muted)]">{formatDate(data.trained_at)}</p>
          </motion.section>

          <motion.section variants={item} className="surface-card p-5">
            <h2 className="mb-3 text-lg font-semibold">Features Used</h2>
            <div className="flex flex-wrap gap-2">
              {data.features_used.map((feature) => (
                <span key={feature} className="rounded-full border border-[var(--color-border)] bg-slate-900 px-3 py-1 text-xs text-slate-300">
                  {feature}
                </span>
              ))}
            </div>
          </motion.section>

          <motion.section variants={item} className="surface-card p-5">
            <h2 className="mb-3 text-lg font-semibold">How This Works</h2>
            <ul className="list-disc space-y-2 pl-6 text-sm text-[var(--color-muted)]">
              <li>You provide property characteristics.</li>
              <li>The model applies learned patterns from 20,000+ California homes.</li>
              <li>It returns an estimated market value in milliseconds.</li>
            </ul>
          </motion.section>
        </motion.div>
      )}
    </div>
  );
}
