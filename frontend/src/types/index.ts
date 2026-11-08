/**
 * Standar penamaan tipe:
 * - Gunakan PascalCase untuk semua interface dan type alias.
 * - Tidak memakai prefix "I" (contoh: `JobSummary`, bukan `IJobSummary`).
 * - Gunakan suffix yang menjelaskan peran: `Props` untuk properti komponen,
 *   `Payload` untuk body request, `Response` untuk body response,
 *   `Params` untuk query/path parameter.
 * - Hindari nama generik seperti `Data` atau `Item` tanpa konteks domain.
 */

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload extends LoginPayload {
  full_name?: string;
}

export interface AuthTokenResponse {
  access_token: string;
  token_type: string;
}

export interface CurrentUser {
  user_id: number;
  email: string;
  full_name: string | null;
  is_admin: boolean;
}

export type JobSort = "score" | "date";

export interface JobSearchParams {
  q?: string;
  category?: string;
  location?: string;
  skill?: string;
  employment_type?: string;
  experience_level?: string;
  sort?: JobSort;
  limit?: number;
  offset?: number;
}

export interface JobSummary {
  job_id: string;
  title: string;
  company: string;
  location: string;
  category: string;
  employment_type: string | null;
  experience_level: string | null;
  is_simulated: boolean;
  match_level: string;
  matched_terms: string[];
  reason: string;
  posted_at: string | null;
}

export interface JobSearchResponse {
  query: string;
  total: number;
  limit: number;
  offset: number;
  sort: JobSort;
  results: JobSummary[];
  message?: string;
}

export interface JobDetail {
  job_id: string;
  title: string;
  description: string;
  company: string;
  location: string;
  category: string | null;
  employment_type: string | null;
  experience_level: string | null;
  source: string | null;
  is_active: boolean;
  is_simulated: boolean;
  skills: string[];
  posted_at: string | null;
}

export type RecommendationSource = "profile" | "latest";

export interface RecommendationItem {
  job_id: string;
  title: string;
  company: string;
  location: string;
  category: string;
  match_level: string;
  source: RecommendationSource;
  reason: string;
  is_simulated: boolean;
  posted_at?: string | null;
}

export interface RecommendationResponse {
  results: RecommendationItem[];
}

export interface BookmarkItem {
  job_id: string;
  title: string;
  company: string;
  location: string;
  category: string;
  is_simulated: boolean;
  posted_at: string | null;
  saved_at: string | null;
}

export interface BookmarkListParams {
  limit?: number;
  offset?: number;
}

export interface BookmarkListResponse {
  items: BookmarkItem[];
  count: number;
  next_offset: number | null;
}

export interface BookmarkCreateResponse extends BookmarkItem {
  created: boolean;
}

export interface BookmarkPayload {
  job_id: string;
}

export interface PreferencesPayload {
  categories: string[];
  locations: string[];
  employment_types: string[];
  experience_levels: string[];
  keywords: string[];
}

export interface PreferencesResponse {
  user_id: number;
  preferences: Partial<PreferencesPayload>;
}

export type EventType = "view" | "click" | "save" | "apply";

export interface EventPayload {
  job_id: string;
  event_type: EventType;
  is_simulated?: boolean;
}

export interface EventResponse {
  event_id: number;
  job_id: string;
  event_type: EventType;
  is_simulated: boolean;
}

export interface EvaluationSummaryResponse {
  queries: number;
  judgments: number;
  runs: number;
  config_hash: string | null;
  dataset_hash: string | null;
}

export interface EvaluationRunResponse {
  detail: string;
  run_id: number;
  report_path: string;
  config_hash: string | null;
  dataset_hash: string | null;
}

export interface ApiErrorBody {
  detail?: string;
}
