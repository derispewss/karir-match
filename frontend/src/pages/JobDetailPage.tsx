import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeftIcon,
  BookmarkCheckIcon,
  BookmarkIcon,
  Building2Icon,
  CalendarIcon,
  InfoIcon,
  MapPinIcon,
} from "lucide-react";
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
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { Spinner } from "@/components/ui/spinner";
import {
  addBookmark,
  fetchBookmarks,
  fetchJobDetail,
  getApiErrorMessage,
  logEvent,
  removeBookmark,
} from "@/lib/api";
import type { JobDetail } from "@/types";

function formatDate(value: string | null): string {
  if (!value) {
    return "Tanggal tidak tersedia";
  }
  return new Date(value).toLocaleDateString("id-ID", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function JobDetailPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const navigate = useNavigate();

  const [job, setJob] = useState<JobDetail | null>(null);
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!jobId) {
      return;
    }

    let isMounted = true;
    setIsLoading(true);
    setError(null);

    Promise.all([
      fetchJobDetail(jobId),
      fetchBookmarks({ limit: 500 }).catch(() => null),
    ])
      .then(([detail, bookmarks]) => {
        if (!isMounted) {
          return;
        }
        setJob(detail);
        setIsBookmarked(
          Boolean(
            bookmarks?.items.some((bookmark) => bookmark.job_id === jobId)
          )
        );
        void logEvent({ job_id: jobId, event_type: "view" }).catch(() => {
          // Event tracking tidak boleh menghalangi tampilan detail.
        });
      })
      .catch((detailError) => {
        if (isMounted) {
          setError(getApiErrorMessage(detailError));
        }
      })
      .finally(() => {
        if (isMounted) {
          setIsLoading(false);
        }
      });

    return () => {
      isMounted = false;
    };
  }, [jobId]);

  const handleToggleBookmark = async () => {
    if (!jobId) {
      return;
    }

    setIsSaving(true);
    try {
      if (isBookmarked) {
        await removeBookmark(jobId);
        setIsBookmarked(false);
        toast.success("Lowongan dihapus dari bookmark.");
      } else {
        const result = await addBookmark(jobId);
        setIsBookmarked(true);
        toast.success(
          result.created
            ? "Lowongan disimpan ke bookmark."
            : "Lowongan sudah ada di bookmark."
        );
      }
    } catch (bookmarkError) {
      toast.error(getApiErrorMessage(bookmarkError));
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col gap-4">
        <Skeleton className="h-8 w-40" />
        <Card>
          <CardHeader className="flex flex-col gap-2">
            <Skeleton className="h-7 w-2/3" />
            <Skeleton className="h-4 w-1/2" />
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </CardContent>
        </Card>
      </div>
    );
  }

  if (error || !job) {
    return (
      <div className="flex flex-col gap-4">
        <Button
          variant="ghost"
          size="sm"
          className="w-fit"
          onClick={() => navigate(-1)}
        >
          <ArrowLeftIcon data-icon="inline-start" />
          Kembali
        </Button>
        <Alert variant="destructive">
          <AlertTitle>Gagal memuat detail lowongan</AlertTitle>
          <AlertDescription>
            {error ?? "Lowongan tidak ditemukan."}
          </AlertDescription>
        </Alert>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <Button
          variant="ghost"
          size="sm"
          className="w-fit"
          onClick={() => navigate(-1)}
        >
          <ArrowLeftIcon data-icon="inline-start" />
          Kembali
        </Button>
        <Button
          variant={isBookmarked ? "secondary" : "default"}
          onClick={() => void handleToggleBookmark()}
          disabled={isSaving}
        >
          {isSaving ? (
            <Spinner />
          ) : isBookmarked ? (
            <BookmarkCheckIcon data-icon="inline-start" />
          ) : (
            <BookmarkIcon data-icon="inline-start" />
          )}
          {isBookmarked ? "Tersimpan" : "Simpan lowongan"}
        </Button>
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_20rem]">
        <Card>
          <CardHeader className="flex flex-col gap-2">
            <div className="flex flex-wrap items-start justify-between gap-2">
              <div className="flex flex-col gap-1">
                <CardTitle className="text-2xl">{job.title}</CardTitle>
                <CardDescription className="flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
                  <span className="inline-flex items-center gap-1">
                    <Building2Icon className="size-3.5" />
                    {job.company}
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <MapPinIcon className="size-3.5" />
                    {job.location}
                  </span>
                </CardDescription>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {job.category ? (
                  <Badge variant="secondary">{job.category}</Badge>
                ) : null}
                {job.employment_type ? (
                  <Badge variant="outline">{job.employment_type}</Badge>
                ) : null}
                {job.experience_level ? (
                  <Badge variant="outline">{job.experience_level}</Badge>
                ) : null}
                {job.is_simulated ? (
                  <Badge variant="secondary">Data simulasi</Badge>
                ) : null}
              </div>
            </div>
            <p className="inline-flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted-foreground">
              <span className="inline-flex items-center gap-1">
                <CalendarIcon className="size-3.5" />
                Diposting {formatDate(job.posted_at)}
              </span>
              <span>Sumber: {job.source ?? "Dataset D1"}</span>
            </p>
          </CardHeader>

          <CardContent className="flex flex-col gap-4">
            {!job.is_active ? (
              <Alert>
                <InfoIcon />
                <AlertTitle>Lowongan tidak aktif</AlertTitle>
                <AlertDescription>
                  Lowongan ini masih dapat dilihat untuk referensi, tetapi tidak
                  ditampilkan pada hasil pencarian dan feed.
                </AlertDescription>
              </Alert>
            ) : null}

            <div className="flex flex-col gap-2">
              <h2 className="text-sm font-semibold">
                Deskripsi dan kualifikasi
              </h2>
              <p className="whitespace-pre-line text-sm leading-relaxed text-muted-foreground">
                {job.description || "Deskripsi belum tersedia."}
              </p>
            </div>

            <Separator />

            <div className="flex flex-col gap-2">
              <h2 className="text-sm font-semibold">Skill yang dicari</h2>
              {job.skills.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {job.skills.map((skill) => (
                    <Badge key={skill} variant="outline">
                      {skill}
                    </Badge>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-muted-foreground">
                  Skill belum dicantumkan.
                </p>
              )}
            </div>
          </CardContent>
        </Card>

        <div className="flex flex-col gap-4">
          <Card size="sm">
            <CardHeader>
              <CardTitle>Catatan kecocokan</CardTitle>
              <CardDescription>
                Tingkat kecocokan menunjukkan relevansi teks, bukan peluang
                diterima.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Alert>
                <InfoIcon />
                <AlertTitle>Bukan probabilitas</AlertTitle>
                <AlertDescription>
                  Sistem tidak menampilkan skor mentah. Gunakan deskripsi dan
                  skill sebagai pertimbangan utama.
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>

          <Card size="sm">
            <CardHeader>
              <CardTitle>Jelajahi lagi</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              <Button variant="outline" render={<Link to="/search" />}>
                Kembali ke pencarian
              </Button>
              <Button variant="ghost" render={<Link to="/feed" />}>
                Lihat rekomendasi
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
