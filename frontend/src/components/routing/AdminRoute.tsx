import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";

import { Spinner } from "@/components/ui/spinner";
import { useAuth } from "@/contexts/AuthContext";

interface AdminRouteProps {
  children: ReactNode;
}

export function AdminRoute({ children }: AdminRouteProps) {
  const { isAdmin, isLoading } = useAuth();

  if (isLoading) {
    return (
      <div className="flex min-h-svh items-center justify-center">
        <Spinner className="size-6" />
      </div>
    );
  }

  if (!isAdmin) {
    return <Navigate to="/search" replace />;
  }

  return children;
}
