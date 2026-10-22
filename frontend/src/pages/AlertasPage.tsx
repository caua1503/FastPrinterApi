import React from "react";
import type { Alerta } from "../types";
import { statusColors } from "../data/mockData";
import { cn } from "../lib/utils";

interface AlertasPageProps {
  alertas: Alerta[];
}

export function AlertasPage({ alertas }: AlertasPageProps) {
  return (
    <div className="bg-white border border-[#e3e7f0] rounded-[14px] p-6 shadow-[0_1px_3px_rgba(20,30,70,0.06)] max-w-4xl">
      <h2 className="text-base font-bold text-[#16224f] mb-4">Central de Alertas e Notificações</h2>
      <div className="divide-y divide-[#e3e7f0]">
        {alertas.map((a, idx) => {
          const colorDot = statusColors[a.tipo]?.dot || "bg-slate-400";
          return (
            <div key={idx} className="flex items-start gap-3.5 py-4 first:pt-2 last:pb-2">
              <span className={cn("w-2.5 h-2.5 rounded-full mt-1.5 shrink-0", colorDot)} />
              <div className="flex-1">
                <div className="text-[13.5px] text-slate-800 leading-snug">{a.texto}</div>
                <div className="text-[11.5px] text-slate-400 mt-1">{a.tempo}</div>
              </div>
            </div>
          );
        })}
        {alertas.length === 0 && (
          <div className="text-center py-10 text-slate-400 text-sm">
            Nenhum alerta ativo no sistema.
          </div>
        )}
      </div>
    </div>
  );
}
