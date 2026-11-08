import { useEffect, useState } from "react";
import { PlayIcon, RefreshCwIcon } from "lucide-react";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Field, FieldDescription, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import {
  fetchEvaluationSummary,
  getApiErrorMessage,
  runEvaluation,
} from "@/lib/api";
import type { EvaluationSummaryResponse } from "@/types";

interface SummaryMetric {
  label: string;
  value: number;
  description: string;
}

export function AdminPage() {
  const [summary, setSummary] = useState<EvaluationSummaryResponse | null>(null);
  const [configPath, setConfigPath] = useState("artifacts");
  const [isLoading, setIsLoading] = useState(true);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [runMessage, setRunMessage] = useState<string | null>(null);

  const loadSummary = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const result = await fetchEvaluationSummary();
      setSummary(result);
    } catch (summaryError) {
      setError(getApiErrorMessage(summaryError));
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void loadSummary();
  }, []);

  const handleRunEvaluation = async () => {
    setIsRunning(true);
    setError(null);
    setRunMessage(null);

    try {
      const result = await runEvaluation(configPath);
      setRunMessage(`${result.detail} (run ID: ${result.run_id})`);
      await loadSummary();
    } catch (runError) {
      setError(getApiErrorMessage(runError));
    } finally {
      setIsRunning(false);
    }
  };

  const metrics: SummaryMetric[] = summary
    ? [
        {
          label: "Query",
          value: summary.queries,
          description: "Jumlah query evaluasi yang tersedia.",
        },
        {
          label: "Judgment",
          value: summary.judgments,
          description: "Total penilaian relevansi dari anotator.",
        },
        {
          label: "Run",
          value: summary.runs,
          description: "Jumlah eksekusi evaluasi yang tercatat.",
        },
      ]
    : [];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">Admin Evaluasi</h1>
        <p className="text-sm text-muted-foreground">
          Pantau data evaluasi dan jalankan ulang benchmark sistem rekomendasi.
        </p>
      </div>

      {error ? (
        <Alert variant="destructive">
          <AlertTitle>Terjadi kesalahan</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      {runMessage ? (
        <Alert>
          <AlertTitle>Evaluasi dijalankan</AlertTitle>
          <AlertDescription>{runMessage}</AlertDescription>
        </Alert>
      ) : null}

      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Ringkasan</h2>
        <Button
          variant="outline"
          onClick={() => void loadSummary()}
          disabled={isLoading}
        >
          <RefreshCwIcon data-icon="inline-start" />
          Muat ulang
        </Button>
      </div>

      <div className="grid gap-3 md:grid-cols-3">
        {isLoading
          ? Array.from({ length: 3 }).map((_, index) => (
              <Card key={index}>
                <CardHeader>
                  <Skeleton className="h-4 w-1/2" />
                </CardHeader>
                <CardContent className="flex flex-col gap-2">
                  <Skeleton className="h-8 w-1/3" />
                  <Skeleton className="h-4 w-full" />
                </CardContent>
              </Card>
            ))
          : metrics.map((metric) => (
              <Card key={metric.label}>
                <CardHeader>
                  <CardDescription>{metric.label}</CardDescription>
                  <CardTitle className="text-3xl">{metric.value}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">
                    {metric.description}
                  </p>
                </CardContent>
              </Card>
            ))}
      </div>

      <Card size="sm">
        <CardHeader>
          <CardTitle>Konteks konfigurasi</CardTitle>
          <CardDescription>
            Hash membantu memastikan hasil evaluasi dapat dilacak ke konfigurasi
            dan dataset yang sama.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-2">
          <div className="flex flex-col gap-1">
            <span className="text-xs font-medium text-muted-foreground">
              Config hash
            </span>
            <span className="font-mono text-xs break-all">
              {summary?.config_hash ?? "Tidak tersedia"}
            </span>
          </div>
          <div className="flex flex-col gap-1">
            <span className="text-xs font-medium text-muted-foreground">
              Dataset hash
            </span>
            <span className="font-mono text-xs break-all">
              {summary?.dataset_hash ?? "Tidak tersedia"}
            </span>
          </div>
        </CardContent>
      </Card>

      <Separator />

      <Card>
        <CardHeader>
          <CardTitle>Jalankan evaluasi</CardTitle>
          <CardDescription>
            Tentukan direktori run evaluasi di dalam folder artifacts.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FieldGroup>
            <Field>
              <FieldLabel htmlFor="eval-config-path">
                Direktori run
              </FieldLabel>
              <Input
                id="eval-config-path"
                value={configPath}
                onChange={(event) => setConfigPath(event.target.value)}
                placeholder="artifacts"
              />
              <FieldDescription>
                Path harus berada di dalam folder artifacts.
              </FieldDescription>
            </Field>
            <Button
              onClick={() => void handleRunEvaluation()}
              disabled={isRunning || !configPath.trim()}
            >
              <PlayIcon data-icon="inline-start" />
              {isRunning ? "Menjalankan..." : "Jalankan evaluasi"}
            </Button>
          </FieldGroup>
        </CardContent>
      </Card>
    </div>
  );
}
