import { useEffect, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { BookmarkIcon, SearchIcon, XIcon } from "lucide-react";
import { toast } from "sonner";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty";
import {
  Field,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { addBookmark, getApiErrorMessage, searchJobs } from "@/lib/api";
import type { JobSearchResponse, JobSort } from "@/types";

const initialSearch: JobSearchResponse = {
  query: "",
  total: 0,
  limit: 10,
  offset: 0,
  sort: "score",
  results: [],
};

interface SearchFilters {
  query: string;
  category: string;
  location: string;
  skill: string;
  employmentType: string;
  experienceLevel: string;
  sort: JobSort;
}

interface ActiveFilter {
  key: keyof SearchFilters;
  label: string;
}

export function SearchPage() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");
  const [skill, setSkill] = useState("");
  const [employmentType, setEmploymentType] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("");
  const [sort, setSort] = useState<JobSort>("score");
  const [response, setResponse] = useState<JobSearchResponse>(initialSearch);
  const [isLoading, setIsLoading] = useState(true);
  const [savingId, setSavingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const filters: SearchFilters = {
    query,
    category,
    location,
    skill,
    employmentType,
    experienceLevel,
    sort,
  };

  const handleSave = async (jobId: string) => {
    setSavingId(jobId);
    try {
      const result = await addBookmark(jobId);
      toast.success(
        result.created
          ? "Lowongan disimpan ke bookmark."
          : "Lowongan sudah ada di bookmark."
      );
    } catch (saveError) {
      toast.error(getApiErrorMessage(saveError));
    } finally {
      setSavingId(null);
    }
  };

  const runSearch = async (
    event?: FormEvent<HTMLFormElement>,
    overrides: Partial<SearchFilters> = {}
  ) => {
    event?.preventDefault();
    const applied = { ...filters, ...overrides };
    setIsLoading(true);
    setError(null);

    try {
      const result = await searchJobs({
        q: applied.query.trim() || undefined,
        category: applied.category.trim() || undefined,
        location: applied.location.trim() || undefined,
        skill: applied.skill.trim() || undefined,
        employment_type: applied.employmentType.trim() || undefined,
        experience_level: applied.experienceLevel.trim() || undefined,
        sort: applied.sort,
        limit: 10,
        offset: 0,
      });
      setResponse(result);
    } catch (searchError) {
      setError(getApiErrorMessage(searchError));
    } finally {
      setIsLoading(false);
    }
  };

  const clearFilter = (key: keyof SearchFilters) => {
    const setters: Record<keyof SearchFilters, (value: string) => void> = {
      query: setQuery,
      category: setCategory,
      location: setLocation,
      skill: setSkill,
      employmentType: setEmploymentType,
      experienceLevel: setExperienceLevel,
      sort: (value) => setSort(value as JobSort),
    };
    setters[key](key === "sort" ? "score" : "");
    void runSearch(undefined, { [key]: key === "sort" ? "score" : "" });
  };

  const resetFilters = () => {
    setQuery("");
    setCategory("");
    setLocation("");
    setSkill("");
    setEmploymentType("");
    setExperienceLevel("");
    setSort("score");
    void runSearch(undefined, {
      query: "",
      category: "",
      location: "",
      skill: "",
      employmentType: "",
      experienceLevel: "",
      sort: "score",
    });
  };

  const allFilters: ActiveFilter[] = [
    { key: "query", label: `Kata kunci: ${query}` },
    { key: "category", label: `Kategori: ${category}` },
    { key: "location", label: `Lokasi: ${location}` },
    { key: "skill", label: `Skill: ${skill}` },
    { key: "employmentType", label: `Tipe: ${employmentType}` },
    { key: "experienceLevel", label: `Level: ${experienceLevel}` },
    { key: "sort", label: `Urutan: ${sort === "score" ? "Relevansi" : "Tanggal"}` },
  ];
  const activeFilters = allFilters.filter((filter) => {
    const value = filters[filter.key];
    return filter.key === "sort" ? value !== "score" : Boolean(value.trim());
  });

  useEffect(() => {
    void runSearch();
    // Pencarian awal hanya dijalankan sekali saat halaman dibuka.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">
          Pencarian Lowongan
        </h1>
        <p className="text-sm text-muted-foreground">
          Cari lowongan berdasarkan kata kunci, kategori, lokasi, dan skill.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Filter pencarian</CardTitle>
          <CardDescription>
            Kombinasikan beberapa filter untuk mempersempit hasil.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={runSearch}>
            <FieldGroup className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              <Field className="md:col-span-2 xl:col-span-1">
                <FieldLabel htmlFor="search-query">Kata kunci</FieldLabel>
                <Input
                  id="search-query"
                  placeholder="Contoh: data analyst"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="search-category">Kategori</FieldLabel>
                <Input
                  id="search-category"
                  placeholder="Contoh: Teknologi"
                  value={category}
                  onChange={(event) => setCategory(event.target.value)}
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="search-location">Lokasi</FieldLabel>
                <Input
                  id="search-location"
                  placeholder="Contoh: Jakarta"
                  value={location}
                  onChange={(event) => setLocation(event.target.value)}
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="search-skill">Skill</FieldLabel>
                <Input
                  id="search-skill"
                  placeholder="Contoh: Python"
                  value={skill}
                  onChange={(event) => setSkill(event.target.value)}
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="search-employment-type">
                  Tipe pekerjaan
                </FieldLabel>
                <Input
                  id="search-employment-type"
                  placeholder="Contoh: Full-Time"
                  value={employmentType}
                  onChange={(event) => setEmploymentType(event.target.value)}
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="search-experience-level">
                  Level pengalaman
                </FieldLabel>
                <Input
                  id="search-experience-level"
                  placeholder="Contoh: Mid-Level"
                  value={experienceLevel}
                  onChange={(event) => setExperienceLevel(event.target.value)}
                />
              </Field>

              <Field>
                <FieldLabel htmlFor="search-sort">Urutkan</FieldLabel>
                <Select
                  value={sort}
                  onValueChange={(value) => setSort(value as JobSort)}
                >
                  <SelectTrigger id="search-sort" className="w-full">
                    <SelectValue placeholder="Pilih urutan" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectGroup>
                      <SelectItem value="score">Relevansi</SelectItem>
                      <SelectItem value="date">Tanggal terbaru</SelectItem>
                    </SelectGroup>
                  </SelectContent>
                </Select>
              </Field>

              <div className="flex items-end">
                <Button type="submit" className="w-full" disabled={isLoading}>
                  <SearchIcon data-icon="inline-start" />
                  Cari lowongan
                </Button>
              </div>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>

      {activeFilters.length > 0 ? (
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-medium text-muted-foreground">
            Filter aktif:
          </span>
          {activeFilters.map((filter) => (
            <Badge
              key={filter.key}
              variant="secondary"
              className="gap-1 pr-1"
            >
              {filter.label}
              <button
                type="button"
                aria-label={`Hapus filter ${filter.label}`}
                className="rounded-sm p-0.5 hover:bg-muted-foreground/20"
                onClick={() => clearFilter(filter.key)}
              >
                <XIcon className="size-3" />
              </button>
            </Badge>
          ))}
          <Button type="button" variant="ghost" size="sm" onClick={resetFilters}>
            Reset semua
          </Button>
        </div>
      ) : null}

      {error ? (
        <Alert variant="destructive">
          <AlertTitle>Pencarian gagal</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <h2 className="text-lg font-semibold">Hasil</h2>
          <Badge variant="secondary">{response.total} lowongan</Badge>
        </div>
      </div>

      <Separator />

      {isLoading ? (
        <div className="flex flex-col gap-3">
          {Array.from({ length: 3 }).map((_, index) => (
            <Card key={index}>
              <CardHeader>
                <Skeleton className="h-5 w-1/3" />
                <Skeleton className="h-4 w-1/2" />
              </CardHeader>
              <CardContent className="flex flex-col gap-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-2/3" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : response.results.length === 0 ? (
        <Empty>
          <EmptyHeader>
            <EmptyMedia variant="icon">
              <SearchIcon />
            </EmptyMedia>
            <EmptyTitle>Tidak ada lowongan ditemukan</EmptyTitle>
            <EmptyDescription>
              Coba ubah kata kunci atau hapus beberapa filter.
            </EmptyDescription>
          </EmptyHeader>
        </Empty>
      ) : (
        <div className="flex flex-col gap-3">
          {response.results.map((job) => (
            <Card key={job.job_id}>
              <CardHeader>
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div className="flex flex-col gap-1">
                    <CardTitle>
                      <Link
                        to={`/jobs/${job.job_id}`}
                        className="underline-offset-4 hover:underline"
                      >
                        {job.title}
                      </Link>
                    </CardTitle>
                    <CardDescription>
                      {job.company} · {job.location}
                    </CardDescription>
                  </div>
                  <Badge variant="secondary">{job.match_level}</Badge>
                </div>
              </CardHeader>
              <CardContent className="flex flex-col gap-3">
                <div className="flex flex-wrap gap-2">
                  <Badge variant="outline">{job.category}</Badge>
                  {job.employment_type ? (
                    <Badge variant="outline">{job.employment_type}</Badge>
                  ) : null}
                  {job.experience_level ? (
                    <Badge variant="outline">{job.experience_level}</Badge>
                  ) : null}
                  {job.is_simulated ? (
                    <Badge variant="secondary">Data simulasi</Badge>
                  ) : null}
                  {job.matched_terms.map((term) => (
                    <Badge key={term} variant="ghost">
                      {term}
                    </Badge>
                  ))}
                </div>
                <p className="text-sm text-muted-foreground">{job.reason}</p>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  {job.posted_at ? (
                    <p className="text-xs text-muted-foreground">
                      Diposting{" "}
                      {new Date(job.posted_at).toLocaleDateString("id-ID", {
                        day: "numeric",
                        month: "long",
                        year: "numeric",
                      })}
                    </p>
                  ) : (
                    <span />
                  )}
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      render={<Link to={`/jobs/${job.job_id}`} />}
                    >
                      Lihat detail
                    </Button>
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => void handleSave(job.job_id)}
                      disabled={savingId === job.job_id}
                    >
                      <BookmarkIcon data-icon="inline-start" />
                      Simpan
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
