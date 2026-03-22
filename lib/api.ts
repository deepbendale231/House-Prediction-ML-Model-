export type PredictionInput = {
  longitude: number;
  latitude: number;
  housing_median_age: number;
  total_rooms: number;
  total_bedrooms: number;
  population: number;
  households: number;
  median_income: number;
  ocean_proximity: string;
};

export type PredictionOutput = {
  predicted_price: number;
  prediction_id: string;
  model_version: string;
  created_at: string;
};

export type PredictionRecord = PredictionOutput & PredictionInput;

export type ModelInfo = {
  version: string;
  rmse: number;
  mae: number;
  r2: number;
  features_used: string[];
  trained_at: string;
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  if (!BASE_URL) {
    throw new ApiError("NEXT_PUBLIC_API_URL is not configured.", 500);
  }

  const response = await fetch(`${BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    let message = "Request failed";
    try {
      const body = await response.json();
      message = body?.detail || body?.message || message;
    } catch {
      message = response.statusText || message;
    }
    throw new ApiError(message, response.status);
  }

  return (await response.json()) as T;
}

export async function predictPrice(input: PredictionInput): Promise<PredictionOutput> {
  return request<PredictionOutput>("/api/v1/predict", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function getPredictionHistory(
  limit = 50,
  offset = 0,
): Promise<PredictionRecord[]> {
  const params = new URLSearchParams({
    limit: String(limit),
    offset: String(offset),
  });
  return request<PredictionRecord[]>(`/api/v1/predictions?${params.toString()}`);
}

export async function getModelInfo(): Promise<ModelInfo> {
  return request<ModelInfo>("/api/v1/model");
}
