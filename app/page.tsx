"use client";

import { motion } from "framer-motion";
import { Loader2, Sparkles } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { ApiError, PredictionInput, PredictionOutput, predictPrice } from "@/lib/api";

const money = new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 });

function AnimatedCurrency({ value }: { value: number }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    let frame = 0;
    const start = performance.now();
    const duration = 1200;

    const tick = (now: number) => {
      const progress = Math.min((now - start) / duration, 1);
      setDisplay(value * progress);
      if (progress < 1) frame = requestAnimationFrame(tick);
    };

    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [value]);

  return <span>{money.format(display)}</span>;
}

export default function PredictPage() {
  const [form, setForm] = useState<PredictionInput>({
    median_income: 8.3,
    housing_median_age: 41,
    ocean_proximity: "NEAR BAY",
    total_rooms: 880,
    total_bedrooms: 129,
    population: 322,
    households: 126,
    longitude: -122.23,
    latitude: 37.88,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionOutput | null>(null);

  const predictionIdShort = useMemo(() => (result ? result.prediction_id.slice(0, 8) : ""), [result]);

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await predictPrice(form);
      setResult(response);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(`${err.message} (HTTP ${err.status})`);
      } else {
        setError("Unexpected error while fetching prediction.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-6xl px-4 md:px-8">
      <div className="mb-8 flex flex-wrap items-center gap-3">
        <h1 className="text-3xl font-extrabold tracking-tight md:text-[36px]">Predict House Value</h1>
        <span className="rounded-full border border-sky-400/40 bg-sky-400/10 px-3 py-1 text-xs font-semibold text-sky-300">
          ML Powered
        </span>
      </div>
      <p className="mb-8 text-[var(--color-muted)]">
        Enter property details to get an instant valuation estimate
      </p>

      <form onSubmit={onSubmit} className="surface-card p-5 md:p-7">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          <section className="space-y-5">
            <label className="block">
              <div className="mb-2 flex items-center justify-between text-sm">
                <span>Median Income</span>
                <span className="text-[var(--color-accent-primary)]">{form.median_income.toFixed(1)}</span>
              </div>
              <input
                type="range"
                min={0.5}
                max={15}
                step={0.1}
                value={form.median_income}
                onChange={(e) => setForm((f) => ({ ...f, median_income: Number(e.target.value) }))}
                className="h-2 w-full cursor-pointer appearance-none rounded-full bg-slate-700 accent-sky-400"
              />
            </label>

            <label className="block">
              <div className="mb-2 flex items-center justify-between text-sm">
                <span>Housing Median Age</span>
                <span className="text-[var(--color-accent-primary)]">{form.housing_median_age}</span>
              </div>
              <input
                type="range"
                min={1}
                max={52}
                step={1}
                value={form.housing_median_age}
                onChange={(e) => setForm((f) => ({ ...f, housing_median_age: Number(e.target.value) }))}
                className="h-2 w-full cursor-pointer appearance-none rounded-full bg-slate-700 accent-indigo-400"
              />
            </label>

            <label className="block text-sm">
              <span className="mb-2 block">Ocean Proximity</span>
              <select
                value={form.ocean_proximity}
                onChange={(e) => setForm((f) => ({ ...f, ocean_proximity: e.target.value }))}
                className="w-full rounded-xl border border-[var(--color-border)] bg-[#0b1220] px-3 py-2 text-[var(--color-text)] outline-none ring-sky-400 focus:ring-2"
              >
                <option>NEAR BAY</option>
                <option>INLAND</option>
                <option>NEAR OCEAN</option>
                <option>ISLAND</option>
                <option>{"<1H OCEAN"}</option>
              </select>
            </label>
          </section>

          <section className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {[
              ["Total Rooms", "total_rooms"],
              ["Total Bedrooms", "total_bedrooms"],
              ["Population", "population"],
              ["Households", "households"],
              ["Longitude", "longitude"],
              ["Latitude", "latitude"],
            ].map(([label, key]) => (
              <label key={key} className="block text-sm">
                <span className="mb-2 block">{label}</span>
                <input
                  type="number"
                  value={form[key as keyof PredictionInput] as number}
                  onChange={(e) =>
                    setForm((f) => ({
                      ...f,
                      [key]: Number(e.target.value),
                    }))
                  }
                  className="w-full rounded-xl border border-[var(--color-border)] bg-[#0b1220] px-3 py-2 text-[var(--color-text)] outline-none ring-sky-400 focus:ring-2"
                  required
                />
              </label>
            ))}
          </section>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-[var(--color-accent-primary)] to-[var(--color-accent-secondary)] px-4 py-3 font-semibold text-slate-950 transition hover:brightness-110 disabled:cursor-not-allowed disabled:opacity-70"
        >
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Analyzing...
            </>
          ) : (
            "Get Valuation"
          )}
        </button>

        {error && <p className="mt-4 text-sm text-rose-400">{error}</p>}
      </form>

      {result && (
        <motion.section
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, ease: "easeOut" }}
          className="mt-8 rounded-2xl border border-sky-300/30 bg-[var(--color-surface)] p-7 shadow-[0_0_40px_rgba(56,189,248,0.3)]"
        >
          <p className="text-sm uppercase tracking-wide text-[var(--color-muted)]">Estimated Market Value</p>
          <div className="mt-2 text-4xl font-black text-[var(--color-accent-primary)] md:text-5xl">
            <AnimatedCurrency value={result.predicted_price} />
          </div>

          <div className="mt-5 flex flex-wrap gap-2">
            <span className="inline-flex items-center gap-1 rounded-full border border-sky-400/30 bg-sky-400/10 px-3 py-1 text-xs text-sky-300">
              <Sparkles className="h-3 w-3" /> {result.model_version}
            </span>
            <span className="rounded-full border border-indigo-400/30 bg-indigo-400/10 px-3 py-1 text-xs text-indigo-300">
              ID: {predictionIdShort}
            </span>
          </div>
        </motion.section>
      )}
    </div>
  );
}
