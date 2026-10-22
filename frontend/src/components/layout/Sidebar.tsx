import React from "react";
import type { PageKey } from "../../types";
import {
  LayoutDashboard,
  Printer,
  Wrench,
  History,
  Bell,
  BarChart3,
  Settings,
  LogOut,
} from "lucide-react";
import { cn } from "../../lib/utils";

interface SidebarProps {
  activePage: PageKey;
  onSelectPage: (page: PageKey) => void;
}

interface NavItemConfig {
  key: PageKey;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

const navItems: NavItemConfig[] = [
  { key: "dashboard", label: "Dashboard", icon: LayoutDashboard },
  { key: "impressoras", label: "Impressoras", icon: Printer },
  { key: "manutencoes", label: "Manutenções", icon: Wrench },
  { key: "recargas", label: "Histórico Recargas", icon: History },
  { key: "alertas", label: "Alertas/Notificações", icon: Bell },
  { key: "relatorios", label: "Relatórios", icon: BarChart3 },
  { key: "configuracoes", label: "Configurações", icon: Settings },
];

export function Sidebar({ activePage, onSelectPage }: SidebarProps) {
  return (
    <aside className="w-[230px] max-md:w-[70px] bg-[#1c2b6b] text-white flex flex-col shrink-0 py-5 transition-all select-none">
      {/* Brand */}
      <div className="font-bold text-[15px] leading-tight px-5 pb-5 border-b border-white/10 mb-3.5 max-md:hidden">
        Sistema de
        <br />
        Impressoras
      </div>

      {/* Navegação */}
      <nav className="flex-1 flex flex-col gap-1 px-2.5">
        {navItems.map((item) => {
          const isActive = activePage === item.key;
          const Icon = item.icon;

          return (
            <button
              key={item.key}
              onClick={() => onSelectPage(item.key)}
              className={cn(
                "flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-[13.5px] transition-colors w-full text-left max-md:justify-center cursor-pointer",
                isActive
                  ? "bg-white text-[#1c2b6b] font-semibold shadow-sm"
                  : "text-white/80 hover:bg-white/10 hover:text-white"
              )}
            >
              <span
                className={cn(
                  "w-[3px] h-3.5 rounded-sm shrink-0 transition-colors max-md:hidden",
                  isActive ? "bg-[#1c2b6b]" : "bg-white/30"
                )}
              />
              <Icon className="w-4 h-4 shrink-0" />
              <span className="truncate max-md:hidden">{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Logout */}
      <div className="px-2.5 pt-3 border-t border-white/10 mt-2.5">
        <button
          onClick={() => alert("Sessão finalizada")}
          className="flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-[12.5px] text-white/60 hover:bg-white/10 hover:text-white transition-colors w-full text-left max-md:justify-center cursor-pointer"
        >
          <LogOut className="w-4 h-4 shrink-0" />
          <span className="truncate max-md:hidden">Sair / Logout</span>
        </button>
      </div>
    </aside>
  );
}
