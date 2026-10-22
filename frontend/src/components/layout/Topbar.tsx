import React from "react";
import type { PageKey } from "../../types";

interface TopbarProps {
  activePage: PageKey;
}

const pageTitles: Record<PageKey, string> = {
  dashboard: "Gerenciamento de Impressoras",
  impressoras: "Impressoras",
  manutencoes: "Manutenções",
  recargas: "Histórico de Recargas",
  alertas: "Alertas e Notificações",
  relatorios: "Relatórios",
  configuracoes: "Configurações",
};

export function Topbar({ activePage }: TopbarProps) {
  const title = pageTitles[activePage] || "Gerenciamento de Impressoras";

  return (
    <header className="h-[62px] bg-white border-b border-[#e3e7f0] flex items-center justify-between px-7 shrink-0">
      <h1 className="text-lg font-bold text-[#16224f] m-0">{title}</h1>
      <div className="flex items-center gap-3">
        <div className="text-right leading-tight">
          <div className="text-[13px] font-semibold text-slate-800">admin</div>
          <div className="text-[11.5px] text-slate-500">Be great</div>
        </div>
        <div className="w-[34px] h-[34px] rounded-full bg-[#f4f6fb] border border-[#e3e7f0] flex items-center justify-center text-[15px] font-medium text-slate-600 select-none">
          A
        </div>
      </div>
    </header>
  );
}
