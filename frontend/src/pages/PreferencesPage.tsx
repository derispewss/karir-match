import { useEffect, useState, type FormEvent } from "react";
import { SaveIcon } from "lucide-react";
import { toast } from "sonner";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Field,
  FieldDescription,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Spinner } from "@/components/ui/spinner";
import {
  fetchPreferences,
  getApiErrorMessage,
  updatePreferences,
} from "@/lib/api";
import type { PreferencesPayload } from "@/types";

interface PreferenceFormState {
  categories: string;
  locations: string;
  employmentTypes: string;
  experienceLevels: string;
  keywords: string;
}

const emptyForm: PreferenceFormState = {
  categories: "",
  locations: "",
  employmentTypes: "",
  experienceLevels: "",
  keywords: "",
};

function joinList(values: string[] | undefined): string {
  return (values ?? []).join(", ");
}

function parseList(value: string): string[] {
  return Array.from(
    new Set(
      value
        .split(",")
        .map((item) => item.trim())
        .filter(Boolean)
    )
  );
}

export function PreferencesPage() {
  const [form, setForm] = useState<PreferenceFormState>(emptyForm);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setIsLoading(true);

    fetchPreferences()
      .then((response) => {
        if (!isMounted) {
          return;
        }
        const preferences = response.preferences;
        setForm({
          categories: joinList(preferences.categories),
          locations: joinList(preferences.locations),
          employmentTypes: joinList(preferences.employment_types),
          experienceLevels: joinList(preferences.experience_levels),
          keywords: joinList(preferences.keywords),
        });
      })
      .catch((loadError) => {
        if (isMounted) {
          setError(getApiErrorMessage(loadError));
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
  }, []);

  const updateField = (key: keyof PreferenceFormState, value: string) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setIsSaving(true);

    const payload: PreferencesPayload = {
      categories: parseList(form.categories),
      locations: parseList(form.locations),
      employment_types: parseList(form.employmentTypes),
      experience_levels: parseList(form.experienceLevels),
      keywords: parseList(form.keywords),
    };

    try {
      await updatePreferences(payload);
      toast.success("Preferensi berhasil disimpan.");
    } catch (saveError) {
      setError(getApiErrorMessage(saveError));
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex flex-col gap-4">
        <Skeleton className="h-8 w-48" />
        <Card>
          <CardHeader className="flex flex-col gap-2">
            <Skeleton className="h-5 w-1/3" />
            <Skeleton className="h-4 w-2/3" />
          </CardHeader>
          <CardContent className="flex flex-col gap-4">
            {Array.from({ length: 4 }).map((_, index) => (
              <Skeleton key={index} className="h-12 w-full" />
            ))}
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight">Preferensi</h1>
        <p className="text-sm text-muted-foreground">
          Preferensi dipakai untuk menyusun feed rekomendasi dan memperkaya
          pencarian Anda.
        </p>
      </div>

      {error ? (
        <Alert variant="destructive">
          <AlertTitle>Terjadi kesalahan</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      ) : null}

      <Card>
        <CardHeader>
          <CardTitle>Preferensi karier</CardTitle>
          <CardDescription>
            Pisahkan beberapa nilai dengan koma. Biarkan kosong bila tidak ada
            preferensi pada bagian tersebut.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <FieldGroup>
              <div className="grid gap-4 md:grid-cols-2">
                <Field>
                  <FieldLabel htmlFor="pref-categories">Kategori</FieldLabel>
                  <Input
                    id="pref-categories"
                    value={form.categories}
                    onChange={(event) =>
                      updateField("categories", event.target.value)
                    }
                    placeholder="Data & Analitik, Teknologi Informasi"
                  />
                  <FieldDescription>
                    Contoh: Data & Analitik, Pemasaran.
                  </FieldDescription>
                </Field>

                <Field>
                  <FieldLabel htmlFor="pref-locations">Lokasi</FieldLabel>
                  <Input
                    id="pref-locations"
                    value={form.locations}
                    onChange={(event) =>
                      updateField("locations", event.target.value)
                    }
                    placeholder="Jakarta Selatan, Remote"
                  />
                  <FieldDescription>
                    Contoh: Bandung, Remote.
                  </FieldDescription>
                </Field>

                <Field>
                  <FieldLabel htmlFor="pref-employment-types">
                    Tipe pekerjaan
                  </FieldLabel>
                  <Input
                    id="pref-employment-types"
                    value={form.employmentTypes}
                    onChange={(event) =>
                      updateField("employmentTypes", event.target.value)
                    }
                    placeholder="Full-Time, Contract"
                  />
                  <FieldDescription>
                    Contoh: Full-Time, Internship, Contract.
                  </FieldDescription>
                </Field>

                <Field>
                  <FieldLabel htmlFor="pref-experience-levels">
                    Level pengalaman
                  </FieldLabel>
                  <Input
                    id="pref-experience-levels"
                    value={form.experienceLevels}
                    onChange={(event) =>
                      updateField("experienceLevels", event.target.value)
                    }
                    placeholder="Entry-Level, Mid-Level"
                  />
                  <FieldDescription>
                    Contoh: Entry-Level, Senior-Level.
                  </FieldDescription>
                </Field>
              </div>

              <Field>
                <FieldLabel htmlFor="pref-keywords">Kata kunci</FieldLabel>
                <Input
                  id="pref-keywords"
                  value={form.keywords}
                  onChange={(event) =>
                    updateField("keywords", event.target.value)
                  }
                  placeholder="data analyst, python, sql"
                />
                <FieldDescription>
                  Kata kunci tambahan untuk personalisasi feed.
                </FieldDescription>
              </Field>

              <Button type="submit" disabled={isSaving}>
                {isSaving ? (
                  <Spinner />
                ) : (
                  <SaveIcon data-icon="inline-start" />
                )}
                Simpan preferensi
              </Button>
            </FieldGroup>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
