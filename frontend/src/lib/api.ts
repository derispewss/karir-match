import axios, {
  type AxiosError,
  type InternalAxiosRequestConfig,
} from "axios";

import type {
  ApiErrorBody,
  AuthTokenResponse,
  BookmarkCreateResponse,
  BookmarkListParams,
  BookmarkListResponse,
  CurrentUser,
  EvaluationRunResponse,
  EvaluationSummaryResponse,
  EventPayload,
  EventResponse,
  JobDetail,
  JobSearchParams,
  JobSearchResponse,
  LoginPayload,
  PreferencesPayload,
  PreferencesResponse,
  RecommendationResponse,
  RegisterPayload,
} from "@/types";

export const TOKEN_STORAGE_KEY = "karirmatch_token";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiErrorBody>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_STORAGE_KEY);
    }
    return Promise.reject(error);
  }
);

export function getApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError<ApiErrorBody>(error)) {
    return error.response?.data?.detail ?? error.message;
  }
  return "Terjadi kesalahan yang tidak diketahui.";
}

export async function loginRequest(
  payload: LoginPayload
): Promise<AuthTokenResponse> {
  const response = await api.post<AuthTokenResponse>("/auth/login", payload);
  return response.data;
}

export async function registerRequest(
  payload: RegisterPayload
): Promise<AuthTokenResponse> {
  const response = await api.post<AuthTokenResponse>("/auth/register", payload);
  return response.data;
}

export async function fetchCurrentUser(): Promise<CurrentUser> {
  const response = await api.get<CurrentUser>("/auth/me");
  return response.data;
}

export async function searchJobs(
  params: JobSearchParams
): Promise<JobSearchResponse> {
  const response = await api.get<JobSearchResponse>("/api/jobs/search", {
    params,
  });
  return response.data;
}

export async function fetchJobDetail(jobId: string): Promise<JobDetail> {
  const response = await api.get<JobDetail>(`/api/jobs/${jobId}`);
  return response.data;
}

export async function fetchPreferences(): Promise<PreferencesResponse> {
  const response = await api.get<PreferencesResponse>("/api/me/preferences");
  return response.data;
}

export async function updatePreferences(
  payload: PreferencesPayload
): Promise<PreferencesResponse> {
  const response = await api.put<PreferencesResponse>(
    "/api/me/preferences",
    payload
  );
  return response.data;
}

export async function fetchBookmarks(
  params: BookmarkListParams = {}
): Promise<BookmarkListResponse> {
  const response = await api.get<BookmarkListResponse>("/api/me/bookmarks", {
    params,
  });
  return response.data;
}

export async function addBookmark(
  jobId: string
): Promise<BookmarkCreateResponse> {
  const response = await api.post<BookmarkCreateResponse>("/api/me/bookmarks", {
    job_id: jobId,
  });
  return response.data;
}

export async function removeBookmark(jobId: string): Promise<void> {
  await api.delete(`/api/me/bookmarks/${jobId}`);
}

export async function logEvent(payload: EventPayload): Promise<EventResponse> {
  const response = await api.post<EventResponse>("/api/events", payload);
  return response.data;
}

export async function fetchRecommendations(): Promise<RecommendationResponse> {
  const response = await api.get<RecommendationResponse>(
    "/api/me/recommendations"
  );
  return response.data;
}

export async function fetchEvaluationSummary(): Promise<EvaluationSummaryResponse> {
  const response = await api.get<EvaluationSummaryResponse>(
    "/api/admin/eval/summary"
  );
  return response.data;
}

export async function runEvaluation(
  configPath: string
): Promise<EvaluationRunResponse> {
  const response = await api.post<EvaluationRunResponse>(
    "/api/admin/eval/run",
    null,
    { params: { config_path: configPath } }
  );
  return response.data;
}

export async function deleteMyData(): Promise<void> {
  await api.delete("/api/me/data");
}

export default api;
