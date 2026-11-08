import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  BookmarkIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  Trash2Icon,
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
import { Spinner } from "@/components/ui/spinner";
import {
  fetchBookmarks,
  getApiErrorMessage,
  removeBookmark,
} from "@/lib/api";
import type { BookmarkListResponse } from "@/types";

const PAGE_SIZE = 20;

const emptyResponse: BookmarkListResponse = {
  items: [],
  count: 0,
  next_offset: null,
};

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

export function BookmarksPage() {
  const [response, setResponse] = useState<BookmarkListResponse>(emptyResponse);
  const [offset, setOffset] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [removingId, setRemovingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const loadBookmarks = async (nextOffset: number) => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await fetchBookmarks({
        limit: PAGE_SIZE,
        offset: nextOffset,
      });
      setResponse(result);
      setOffset(nextOffset);
    } catch (loadError) {
      setError(getApiErrorMessage(loadError));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void loadBookmarks(0);
  }, []);

  const handleRemove = async (jobId: string) => {
    setRemovingId(jobId);
    try {
      await removeBookmark(jobId);
      toast.success("Bookmark dihapus.");
      const nextOffset =
        response.items.length === 1 && offset > 0
          ? Math.max(offset - PAGE_SIZE, 0)
          : offset;
      await loadBookmarks(nextOffset);
    } catch (removeError) {
      toast.error(getApiErrorMessage(removeError));
    } finally {
      setRemovingId(null);
    }
  };

  const hasPrevious = offset > 0;
  const hasNext = response.next_offset !== null;

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">Bookmark</h1>
        <p className="text-sm text-muted-foreground">
          Lowongan yang Anda simpan untuk ditinjau kembali.
        </p>
      </div>

      {error ? (
        <Alert variant="destructive">
          <AlertTitle>Gagal memuat bookmark</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <h2 className="text-lg font-semibold">Daftar tersimpan</h2>
          <Badge variant="secondary">{response.count} lowongan</Badge>
        </div>
        <Button
          variant="outline"
          onClick={() => void loadBookmarks(offset)}
          disabled={isLoading}
        >
          Muat ulang
        </Button>
      </div>

      <Separator />

      {isLoading ? (
        <div className="grid gap-3 lg:grid-cols-2">
          {Array.from({ length: 4 }).map((_, index) => (
            <Card key={index}>
              <CardHeader className="flex flex-col gap-2">
                <Skeleton className="h-5 w-1/2" />
                <Skeleton className="h-4 w-2/3" />
              </CardHeader>
              <CardContent className="flex flex-col gap-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-1/3" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : response.items.length === 0 ? (
        <Empty>
          <EmptyHeader>
            <EmptyMedia variant="icon">
              <BookmarkIcon />
            </EmptyMedia>
            <EmptyTitle>Belum ada bookmark</EmptyTitle>
            <EmptyDescription>
              Simpan lowongan dari halaman pencarian atau detail lowongan untuk
              melihatnya di sini.
            </EmptyDescription>
          </EmptyHeader>
          <EmptyContent>
            <Button render={<Link to="/search" />}>Cari lowongan</Button>
          </EmptyContent>
        </Empty>
      ) : (
        <div className="grid gap-3 lg:grid-cols-2">
          {response.items.map((item) => (
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
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge variant="secondary">{item.category}</Badge>
                    {item.is_simulated ? (
                      <Badge variant="outline">Data simulasi</Badge>
                    ) : null}
                  </div>
                </div>
              </CardHeader>
              <CardContent className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-xs text-muted-foreground">
                  Disimpan {formatDate(item.saved_at)}
                </p>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    render={<Link to={`/jobs/${item.job_id}`} />}
                  >
                    Lihat detail
                  </Button>
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => void handleRemove(item.job_id)}
                    disabled={removingId === item.job_id}
                  >
                    {removingId === item.job_id ? (
                      <Spinner />
                    ) : (
                      <Trash2Icon data-icon="inline-start" />
                    )}
                    Hapus
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {response.count > PAGE_SIZE ? (
        <div className="flex items-center justify-between">
          <p className="text-xs text-muted-foreground">
            Menampilkan {offset + 1}–
            {Math.min(offset + PAGE_SIZE, response.count)} dari {response.count}
          </p>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => void loadBookmarks(Math.max(offset - PAGE_SIZE, 0))}
              disabled={!hasPrevious || isLoading}
            >
              <ChevronLeftIcon data-icon="inline-start" />
              Sebelumnya
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => void loadBookmarks(response.next_offset ?? offset)}
              disabled={!hasNext || isLoading}
            >
              Berikutnya
              <ChevronRightIcon data-icon="inline-end" />
            </Button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
