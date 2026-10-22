import React, { useState } from "react";

export function ConfiguracoesPage() {
  const [username, setUsername] = useState("admin");
  const [email, setEmail] = useState("admin@empresa.com");
  const [threshold, setThreshold] = useState(20);
  const [frequency, setFrequency] = useState("Tempo real");
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="bg-white border border-[#e3e7f0] rounded-[14px] p-6 shadow-[0_1px_3px_rgba(20,30,70,0.06)] max-w-lg">
      <form onSubmit={handleSave} className="space-y-6">
        {/* Seção Perfil */}
        <div>
          <h3 className="text-sm font-bold text-[#16224f] mb-3 pb-1 border-b border-[#e3e7f0]">
            Perfil
          </h3>
          <div className="space-y-3.5">
            <div className="flex flex-col gap-1.5 max-w-sm">
              <label className="text-[12.5px] font-semibold text-slate-500">
                Nome de usuário
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="px-3 py-2 bg-white border border-[#e3e7f0] rounded-lg text-[13px] outline-none focus:border-[#28398c] transition-colors"
              />
            </div>
            <div className="flex flex-col gap-1.5 max-w-sm">
              <label className="text-[12.5px] font-semibold text-slate-500">
                E-mail
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="px-3 py-2 bg-white border border-[#e3e7f0] rounded-lg text-[13px] outline-none focus:border-[#28398c] transition-colors"
              />
            </div>
          </div>
        </div>

        {/* Seção Notificações */}
        <div>
          <h3 className="text-sm font-bold text-[#16224f] mb-3 pb-1 border-b border-[#e3e7f0]">
            Notificações
          </h3>
          <div className="space-y-3.5">
            <div className="flex flex-col gap-1.5 max-w-sm">
              <label className="text-[12.5px] font-semibold text-slate-500">
                Alertar quando nível de insumo for menor que (%)
              </label>
              <input
                type="number"
                min={1}
                max={100}
                value={threshold}
                onChange={(e) => setThreshold(Number(e.target.value))}
                className="px-3 py-2 bg-white border border-[#e3e7f0] rounded-lg text-[13px] outline-none focus:border-[#28398c] transition-colors"
              />
            </div>
            <div className="flex flex-col gap-1.5 max-w-sm">
              <label className="text-[12.5px] font-semibold text-slate-500">
                Frequência de verificação
              </label>
              <select
                value={frequency}
                onChange={(e) => setFrequency(e.target.value)}
                className="px-3 py-2 bg-white border border-[#e3e7f0] rounded-lg text-[13px] outline-none focus:border-[#28398c] transition-colors"
              >
                <option value="Tempo real">Tempo real</option>
                <option value="A cada hora">A cada hora</option>
                <option value="Diariamente">Diariamente</option>
              </select>
            </div>
          </div>
        </div>

        {/* Feedback & Botão Salvar */}
        <div className="pt-2 flex items-center gap-3">
          <button
            type="submit"
            className="bg-[#1c2b6b] hover:bg-[#28398c] text-white px-5 py-2.5 rounded-lg text-[13px] font-semibold transition-colors cursor-pointer"
          >
            Salvar alterações
          </button>
          {saved && (
            <span className="text-xs font-semibold text-emerald-600 animate-fade-in">
              Alterações salvas com sucesso!
            </span>
          )}
        </div>
      </form>
    </div>
  );
}
