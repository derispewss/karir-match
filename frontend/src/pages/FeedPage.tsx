import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  BookmarkIcon,
  BriefcaseBusinessIcon,
  SparklesIcon,
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
import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import {
  addBookmark,
  fetchRecommendations,
  getApiErrorMessage,
} from "@/lib/api";
import type { RecommendationItem } from "@/types";

export function FeedPage() {
  const [items, setItems] = useState<RecommendationItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [savingId, setSavingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

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

  const loadFeed = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetchRecommendations();
      setItems(response.results);
    } catch (feedError) {
      setError(getApiErrorMessage(feedError));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void loadFeed();
  }, []);

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">
          Rekomendasi untuk Anda
        </h1>
        <p className="text-sm text-muted-foreground">
          Lowongan yang dipersonalisasi berdasarkan profil dan preferensi Anda.
        </p>
      </div>

      {error ? (
        <Alert variant="destructive">
          <AlertTitle>Gagal memuat rekomendasi</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <h2 className="text-lg font-semibold">Pilihan teratas</h2>
          <Badge variant="secondary">{items.length} lowongan</Badge>
        </div>
        <Button variant="outline" onClick={() => void loadFeed()} disabled={isLoading}>
          <SparklesIcon data-icon="inline-start" />
          Muat ulang
        </Button>
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
      ) : items.length === 0 ? (
        <Empty>
          <EmptyHeader>
            <EmptyMedia variant="icon">
              <BriefcaseBusinessIcon />
            </EmptyMedia>
            <EmptyTitle>Belum ada rekomendasi</EmptyTitle>
            <EmptyDescription>
              Lengkapi preferensi atau simpan beberapa lowongan agar sistem
              dapat mempelajari minat Anda.
            </EmptyDescription>
          </EmptyHeader>
          <EmptyContent>
            <Button variant="outline" onClick={() => void loadFeed()}>
              Coba lagi
            </Button>
          </EmptyContent>
        </Empty>
      ) : (
        <div className="grid gap-3 lg:grid-cols-2">
          {items.map((item) => (
            <Card key={item.job_id}>
              <CardHeader>
                <div className="flex flex-wrap items-start justify-between gap-2">
                  <div className="flex flex-col gap-1">
                    <CardTitle>
                      <Link
                        to={`/jobs/${item.job_id}`}
                        className="underline-offset-4 hover:underline"
                      >
                        {item.title}
                      </Link>
                    </CardTitle>
                    <CardDescription>
                      {item.company} · {item.location}
                    </CardDescription>
                  </div>
                  <Badge variant="secondary">{item.match_level}</Badge>
                </div>
              </CardHeader>
              <CardContent className="flex flex-col gap-3">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge variant="outline">{item.category}</Badge>
                  <Badge
                    variant={item.source === "profile" ? "default" : "ghost"}
                  >
                    {item.source === "profile"
                      ? "Dipersonalisasi"
                      : "Lowongan terbaru"}
                  </Badge>
                  {item.is_simulated ? (
                    <Badge variant="secondary">Data simulasi</Badge>
                  ) : null}
                </div>
                <p className="text-sm text-muted-foreground">{item.reason}</p>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  {item.posted_at ? (
                    <p className="text-xs text-muted-foreground">
                      Diposting{" "}
                      {new Date(item.posted_at).toLocaleDateString("id-ID", {
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
                      render={<Link to={`/jobs/${item.job_id}`} />}
                    >
                      Lihat detail
                    </Button>
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => void handleSave(item.job_id)}
                      disabled={savingId === item.job_id}
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
