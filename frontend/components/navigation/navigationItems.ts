export type NavigationItem = {
  label: string;
  icon: string;
  href: string;
};

export type NavigationSection = {
  title: string;
  items: NavigationItem[];
};

export const navigationSections: NavigationSection[] = [
  {
    title: "Workspace",
    items: [
      {
        label: "Dashboard",
        icon: "⌂",
        href: "/",
      },
    ],
  },

  {
    title: "Workforce",
    items: [
      {
        label: "Employees",
        icon: "👥",
        href: "/employees",
      },
      {
        label: "Attendance",
        icon: "◷",
        href: "/attendance",
      },
      {
        label: "Leave",
        icon: "🌴",
        href: "/leave",
      },
      {
        label: "Payroll",
        icon: "₱",
        href: "/payroll",
      },
    ],
  },

  {
    title: "Management",
    items: [
      {
        label: "HR",
        icon: "▣",
        href: "/hr",
      },
      {
        label: "Recruitment",
        icon: "◉",
        href: "/recruitment",
      },
      {
        label: "Reports",
        icon: "▤",
        href: "/reports",
      },
    ],
  },

  {
    title: "System",
    items: [
      {
        label: "Notifications",
        icon: "♢",
        href: "/notifications",
      },
      {
        label: "Settings",
        icon: "⚙",
        href: "/settings",
      },
    ],
  },
];