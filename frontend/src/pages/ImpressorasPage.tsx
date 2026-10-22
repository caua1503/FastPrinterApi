import React, { useState, useMemo } from "react";
import type { Printer } from "../types";
import { StatusDot } from "../components/ui/StatusBadge";
import { Search, Plus } from "lucide-react";

interface ImpressorasPageProps {
  printers: Printer[];
  onAddPrinter?: () => void;
}

export function ImpressorasPage({ printers, onAddPrinter }: ImpressorasPageProps) {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredPrinters = useMemo(() => {
    const term = searchTerm.toLowerCase().trim();
    if (!term) return printers;
    return printers.filter(
      (p) =>
        p.nome.toLowerCase().includes(term) ||
        p.setor.toLowerCase().includes(term) ||
        p.local.toLowerCase().includes(term) ||
        p.modelo.toLowerCase().includes(term)
    );
  }, [printers, searchTerm]);

  return (
    <div className="space-y-5">
      {/* Barra de Ações: Busca e Botão Novo */}
      <div className="flex justify-between items-center gap-3">
        <div className="relative flex-1 max-w-xs">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar impressora..."
            className="w-full pl-9 pr-3 py-2 bg-white border border-[#e3e7f0] rounded-lg text-[13px] outline-none focus:border-[#28398c] transition-colors"
          />
        </div>
        <button
          onClick={onAddPrinter || (() => alert("Modal de cadastro de impressora"))}
          className="flex items-center gap-1.5 bg-[#1c2b6b] hover:bg-[#28398c] text-white px-4 py-2 rounded-lg text-[13px] font-semibold transition-colors cursor-pointer"
        >
          <Plus className="w-4 h-4" />
          <span>Nova impressora</span>
        </button>
      </div>

      {/* Grid de Cards de Impressoras */}
      <div className="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-4">
        {filteredPrinters.map((p) => (
          <div
            key={p.id}
            className="bg-white border border-[#1d2333]/70 rounded-md p-5 transition-all hover:shadow-[0_6px_18px_rgba(20,30,70,0.08)] hover:-translate-y-0.5"
          >
            <div className="font-bold text-[14.5px] text-[#1d2333] mb-3.5 truncate" title={p.nome}>
              {p.nome}
            </div>

            <div className="flex items-center gap-1.5 text-[12.5px] text-[#1d2333] mb-2 leading-relaxed">
              <span className="font-bold shrink-0">Status:</span>
              <StatusDot status={p.status} />
            </div>

            <div className="flex items-center gap-1.5 text-[12.5px] text-[#1d2333] mb-2 leading-relaxed">
              <span className="font-bold shrink-0">Setor:</span>
              <span className="text-slate-500">{p.setor}</span>
            </div>

            <div className="flex items-center gap-1.5 text-[12.5px] text-[#1d2333] mb-2 leading-relaxed">
              <span className="font-bold shrink-0">Porcentagem:</span>
              <span className="text-slate-500">{p.nivel}%</span>
            </div>

            <div className="flex items-center gap-1.5 text-[12.5px] text-[#1d2333] mb-2 leading-relaxed">
              <span className="font-bold shrink-0">Previsão:</span>
              <span className="text-slate-500">{p.previsao}</span>
            </div>

            <div className="border-t border-[#e3e7f0] my-2.5" />

            <div className="flex items-center gap-1.5 text-[12.5px] text-[#1d2333] mb-2 leading-relaxed">
              <span className="font-bold shrink-0">Última recarga:</span>
              <span className="text-slate-500">{p.ultimaRecarga}</span>
            </div>

            <div className="flex items-center gap-1.5 text-[12.5px] text-[#1d2333] mb-2 leading-relaxed">
              <span className="font-bold shrink-0">Última manutenção:</span>
              <span className="text-slate-500">{p.ultimaManutencao}</span>
            </div>

            <div className="flex items-center gap-1.5 text-[12.5px] text-[#1d2333] leading-relaxed">
              <span className="font-bold shrink-0">Última verificação:</span>
              <span className="text-slate-500">{p.ultimaVerificacao}</span>
            </div>
          </div>
        ))}

        {filteredPrinters.length === 0 && (
          <div className="col-span-full bg-white border border-[#e3e7f0] rounded-xl p-10 text-center text-slate-400 text-sm">
            Nenhuma impressora encontrada para &quot;{searchTerm}&quot;.
          </div>
        )}
      </div>
    </div>
  );
}
