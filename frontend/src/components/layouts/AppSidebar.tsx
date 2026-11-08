import {
  BookmarkIcon,
  BriefcaseBusinessIcon,
  LayoutDashboardIcon,
  LogOutIcon,
  SearchIcon,
  Settings2Icon,
  ShieldCheckIcon,
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
} from "@/components/ui/sidebar";
import { useAuth } from "@/contexts/AuthContext";

interface NavigationItem {
  title: string;
  url: string;
  icon: typeof SearchIcon;
  adminOnly?: boolean;
}

const navigationItems: NavigationItem[] = [
  {
    title: "Pencarian",
    url: "/search",
    icon: SearchIcon,
  },
  {
    title: "Rekomendasi",
    url: "/feed",
    icon: BriefcaseBusinessIcon,
  },
  {
    title: "Bookmark",
    url: "/bookmarks",
    icon: BookmarkIcon,
  },
  {
    title: "Preferensi",
    url: "/preferences",
    icon: Settings2Icon,
  },
  {
    title: "Admin",
    url: "/admin",
    icon: ShieldCheckIcon,
    adminOnly: true,
  },
];

function getInitials(fullName: string | null, email: string): string {
  if (fullName?.trim()) {
    return fullName
      .split(" ")
      .slice(0, 2)
      .map((part) => part[0])
      .join("")
      .toUpperCase();
  }
  return email.slice(0, 2).toUpperCase();
}

export function AppSidebar() {
  const { pathname } = useLocation();
  const { user, isAdmin, logout } = useAuth();

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-1">
          <div className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <LayoutDashboardIcon />
          </div>
          <div className="flex flex-col group-data-[collapsible=icon]:hidden">
            <span className="text-sm font-semibold">KarirMatch</span>
            <span className="text-xs text-muted-foreground">
              Rekomendasi karier
            </span>
          </div>
        </div>
      </SidebarHeader>

      <SidebarSeparator />

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Menu utama</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems
                .filter((item) => !item.adminOnly || isAdmin)
                .map((item) => (
                  <SidebarMenuItem key={item.url}>
                    <SidebarMenuButton
                      render={<Link to={item.url} />}
                      isActive={
                        pathname === item.url ||
                        (item.url === "/search" &&
                          pathname.startsWith("/jobs/"))
                      }
                      tooltip={item.title}
                    >
                      <item.icon />
                      <span>{item.title}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>

      <SidebarFooter>
        <SidebarSeparator />
        <div className="flex items-center gap-2 px-2 py-1">
          <Avatar size="sm">
            <AvatarFallback>
              {user ? getInitials(user.full_name, user.email) : "KM"}
            </AvatarFallback>
          </Avatar>
          <div className="flex min-w-0 flex-col group-data-[collapsible=icon]:hidden">
            <span className="truncate text-sm font-medium">
              {user?.full_name ?? "Pengguna"}
            </span>
            <span className="truncate text-xs text-muted-foreground">
              {user?.email}
            </span>
          </div>
          {isAdmin ? (
            <Badge variant="secondary" className="ml-auto group-data-[collapsible=icon]:hidden">
              Admin
            </Badge>
          ) : null}
        </div>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton onClick={logout} tooltip="Keluar">
              <LogOutIcon />
              <span>Keluar</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>

      <SidebarRail />
    </Sidebar>
  );
}
