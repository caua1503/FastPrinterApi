import React from "react";
import type { Printer, Recarga, Alerta, PrinterStatus } from "../types";
import { statusColors } from "../data/mockData";
import { cn } from "../lib/utils";

interface DashboardPageProps {
  printers: Printer[];
  recargas: Recarga[];
  alertas: Alerta[];
}

export function DashboardPage({ printers, recargas, alertas }: DashboardPageProps) {
  const countStatus = (status: PrinterStatus) =>
    printers.filter((p) => p.status === status).length;

  const statusCards = [
    { key: "excelente", label: "Excelentes", count: countStatus("excelente"), topBorder: "bg-[#1f9d55]" },
    { key: "bom", label: "Bom", count: countStatus("bom"), topBorder: "bg-[#2f7fd6]" },
    { key: "ruim", label: "Ruim", count: countStatus("ruim"), topBorder: "bg-[#e3a008]" },
    { key: "critico", label: "Crítico", count: countStatus("critico"), topBorder: "bg-[#d64545]" },
  ] as const;

  return (
    <div className="space-y-7">
      {/* Cards de Status */}
      <div className="grid grid-cols-4 max-md:grid-cols-2 gap-4">
        {statusCards.map((card) => (
          <div
            key={card.key}
            className="bg-white border border-[#e3e7f0] rounded-[14px] p-5 text-center shadow-[0_1px_3px_rgba(20,30,70,0.06),0_8px_20px_rgba(20,30,70,0.04)] relative overflow-hidden"
          >
            <div className={cn("absolute top-0 left-0 right-0 h-1", card.topBorder)} />
            <div className="text-[11px] font-bold tracking-wider text-slate-500 uppercase mb-2.5">
              {card.label}
            </div>
            <div className="text-4xl font-bold text-[#16224f]">{card.count}</div>
          </div>
        ))}
      </div>

      {/* Linha dupla: Recargas e Alertas */}
      <div className="grid grid-cols-1 lg:grid-cols-[1.4fr_1fr] gap-5">
        {/* Painel: Últimas Recargas */}
        <div className="bg-white border border-[#e3e7f0] rounded-[14px] p-5 shadow-[0_1px_3px_rgba(20,30,70,0.06)]">
          <h2 className="text-[15px] font-bold text-[#16224f] text-center mb-4 tracking-wide uppercase">
            Últimas Recargas
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full text-[13px] border-collapse">
              <thead>
                <tr className="border-b-2 border-[#e3e7f0]">
                  <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                    ID
                  </th>
                  <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                    Nome
                  </th>
                  <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                    Data
                  </th>
                  <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                    Tipo Insumo
                  </th>
                  <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                    Insumo
                  </th>
                </tr>
              </thead>
              <tbody>
                {recargas.slice(0, 5).map((r) => (
                  <tr key={r.id} className="border-b border-[#e3e7f0] hover:bg-[#fafbfd] transition-colors">
                    <td className="py-2.5 px-3 text-slate-800">{r.id}</td>
                    <td className="py-2.5 px-3 text-slate-800 font-medium">{r.nome}</td>
                    <td className="py-2.5 px-3 text-slate-600">{r.data}</td>
                    <td className="py-2.5 px-3 text-slate-600">{r.tipo}</td>
                    <td className="py-2.5 px-3 text-slate-600">{r.insumo}</td>
                  </tr>
                ))}
                {recargas.length === 0 && (
                  <tr>
                    <td colSpan={5} className="text-center py-8 text-slate-400">
                      Nenhuma recarga registrada ainda.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Painel: Alertas Recentes */}
        <div className="bg-white border border-[#e3e7f0] rounded-[14px] p-5 shadow-[0_1px_3px_rgba(20,30,70,0.06)]">
          <h2 className="text-[15px] font-bold text-[#16224f] text-center mb-4 tracking-wide uppercase">
            Alertas Recentes
          </h2>
          <div className="divide-y divide-[#e3e7f0]">
            {alertas.slice(0, 4).map((a, idx) => {
              const colorDot = statusColors[a.tipo]?.dot || "bg-slate-400";
              return (
                <div key={idx} className="flex gap-3 py-3 first:pt-0 last:pb-0 items-start">
                  <span className={cn("w-2.5 h-2.5 rounded-full mt-1.5 shrink-0", colorDot)} />
                  <div>
                    <div className="text-[13px] text-slate-800 leading-snug">{a.texto}</div>
                    <div className="text-[11.5px] text-slate-400 mt-0.5">{a.tempo}</div>
                  </div>
                </div>
              );
            })}
            {alertas.length === 0 && (
              <div className="text-center py-8 text-slate-400 text-sm">
                Nenhum alerta recente no momento.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
