import { createBrowserRouter, Navigate } from "react-router-dom";

import { AppLayout } from "@/components/layouts/AppLayout";
import { AdminRoute } from "@/components/routing/AdminRoute";
import { ProtectedRoute } from "@/components/routing/ProtectedRoute";
import { AdminPage } from "@/pages/AdminPage";
import { BookmarksPage } from "@/pages/BookmarksPage";
import { FeedPage } from "@/pages/FeedPage";
import { JobDetailPage } from "@/pages/JobDetailPage";
import { LoginPage } from "@/pages/LoginPage";
import { PreferencesPage } from "@/pages/PreferencesPage";
import { SearchPage } from "@/pages/SearchPage";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <AppLayout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/search" replace />,
      },
      {
        path: "search",
        element: <SearchPage />,
      },
      {
        path: "jobs/:jobId",
        element: <JobDetailPage />,
      },
      {
        path: "feed",
        element: <FeedPage />,
      },
      {
        path: "bookmarks",
        element: <BookmarksPage />,
      },
      {
        path: "preferences",
        element: <PreferencesPage />,
      },
      {
        path: "admin",
        element: (
          <AdminRoute>
            <AdminPage />
          </AdminRoute>
        ),
      },
    ],
  },
  {
    path: "*",
    element: <Navigate to="/search" replace />,
  },
]);
