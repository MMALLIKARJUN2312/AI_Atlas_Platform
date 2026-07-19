import {
  Building2,
  BrainCircuit,
  Newspaper,
  Shield,
  Compass,
} from "lucide-react";

export const navigation = [
  {
    href: "/",
    label: "Discover",
    icon: Compass,
  },
  {
    href: "/companies",
    label: "Companies",
    icon: Building2,
  },
  {
    href: "/ask-ai",
    label: "Ask AI",
    icon: BrainCircuit,
  },
  {
    href: "/news",
    label: "News",
    icon: Newspaper,
  },
  {
    href: "/admin",
    label: "Admin",
    icon: Shield,
  },
];