import React from "react";
import type { Printer, Recarga, Manutencao, PrinterStatus } from "../types";
import { StatusBadge } from "../components/ui/StatusBadge";

interface RelatoriosPageProps {
  printers: Printer[];
  recargas: Recarga[];
  manutencoes: Manutencao[];
}

export function RelatoriosPage({ printers, recargas, manutencoes }: RelatoriosPageProps) {
  const countStatus = (status: PrinterStatus) =>
    printers.filter((p) => p.status === status).length;

  const kpis = [
    { label: "Total de impressoras", value: printers.length },
    { label: "Recargas no mês", value: recargas.length },
    { label: "Manutenções no mês", value: manutencoes.length },
  ];

  const statuses: PrinterStatus[] = ["excelente", "bom", "ruim", "critico"];

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Linha de KPIs */}
      <div className="grid grid-cols-3 max-md:grid-cols-1 gap-4">
        {kpis.map((kpi, idx) => (
          <div
            key={idx}
            className="bg-white border border-[#e3e7f0] rounded-[14px] p-5 shadow-[0_1px_3px_rgba(20,30,70,0.06)]"
          >
            <div className="text-[11.5px] text-slate-500 uppercase tracking-wider font-semibold mb-2">
              {kpi.label}
            </div>
            <div className="text-3xl font-bold text-[#16224f]">{kpi.value}</div>
          </div>
        ))}
      </div>

      {/* Tabela de Resumo por Status */}
      <div className="bg-white border border-[#e3e7f0] rounded-[14px] p-5 shadow-[0_1px_3px_rgba(20,30,70,0.06)]">
        <h2 className="text-[15px] font-bold text-[#16224f] text-center mb-4 tracking-wide uppercase">
          Resumo por Status
        </h2>
        <div className="overflow-x-auto">
          <table className="w-full text-[13px] border-collapse">
            <thead>
              <tr className="border-b-2 border-[#e3e7f0]">
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  Status
                </th>
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  Quantidade
                </th>
              </tr>
            </thead>
            <tbody>
              {statuses.map((status) => (
                <tr key={status} className="border-b border-[#e3e7f0] hover:bg-[#fafbfd] transition-colors">
                  <td className="py-2.5 px-3">
                    <StatusBadge status={status} />
                  </td>
                  <td className="py-2.5 px-3 text-slate-800 font-medium">
                    {countStatus(status)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
