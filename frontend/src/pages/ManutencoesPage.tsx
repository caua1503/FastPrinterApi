import React, { useState, useMemo } from "react";
import type { Manutencao } from "../types";
import { Search, Plus } from "lucide-react";

interface ManutencoesPageProps {
  manutencoes: Manutencao[];
  onAddManutencao?: () => void;
}

export function ManutencoesPage({ manutencoes, onAddManutencao }: ManutencoesPageProps) {
  const [searchTerm, setSearchTerm] = useState("");

  const filtered = useMemo(() => {
    const term = searchTerm.toLowerCase().trim();
    if (!term) return manutencoes;
    return manutencoes.filter(
      (m) =>
        m.nome.toLowerCase().includes(term) ||
        m.tipo.toLowerCase().includes(term) ||
        m.tecnico.toLowerCase().includes(term) ||
        m.status.toLowerCase().includes(term)
    );
  }, [manutencoes, searchTerm]);

  return (
    <div className="space-y-5">
      {/* Barra de Ações */}
      <div className="flex justify-between items-center gap-3">
        <div className="relative flex-1 max-w-xs">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar manutenção..."
            className="w-full pl-9 pr-3 py-2 bg-white border border-[#e3e7f0] rounded-lg text-[13px] outline-none focus:border-[#28398c] transition-colors"
          />
        </div>
        <button
          onClick={onAddManutencao || (() => alert("Modal para agendar manutenção"))}
          className="flex items-center gap-1.5 bg-[#1c2b6b] hover:bg-[#28398c] text-white px-4 py-2 rounded-lg text-[13px] font-semibold transition-colors cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>Agendar manutenção</span>
        </button>
      </div>

      {/* Tabela de Manutenções */}
      <div className="bg-white border border-[#e3e7f0] rounded-[14px] p-5 shadow-[0_1px_3px_rgba(20,30,70,0.06)]">
        <div className="overflow-x-auto">
          <table className="w-full text-[13px] border-collapse">
            <thead>
              <tr className="border-b-2 border-[#e3e7f0]">
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  ID
                </th>
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  Impressora
                </th>
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  Tipo
                </th>
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  Data
                </th>
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  Técnico
                </th>
                <th className="text-left py-2.5 px-3 text-slate-500 font-semibold text-[11.5px] uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((m) => (
                <tr key={m.id} className="border-b border-[#e3e7f0] hover:bg-[#fafbfd] transition-colors">
                  <td className="py-3 px-3 text-slate-800">{m.id}</td>
                  <td className="py-3 px-3 text-slate-800 font-medium">{m.nome}</td>
                  <td className="py-3 px-3 text-slate-600">{m.tipo}</td>
                  <td className="py-3 px-3 text-slate-600">{m.data}</td>
                  <td className="py-3 px-3 text-slate-600">{m.tecnico}</td>
                  <td className="py-3 px-3">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        m.status === "Concluída"
                          ? "bg-emerald-50 text-emerald-700"
                          : m.status === "Em andamento"
                          ? "bg-amber-50 text-amber-700"
                          : "bg-blue-50 text-blue-700"
                      }`}
                    >
                      {m.status}
                    </span>
                  </td>
                </tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={6} className="text-center py-8 text-slate-400">
                    Nenhuma manutenção encontrada.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
