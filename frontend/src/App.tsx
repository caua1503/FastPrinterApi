import React, { useState } from "react";
import type { PageKey } from "./types";
import {
  initialPrinters,
  initialRecargas,
  initialManutencoes,
  initialAlertas,
} from "./data/mockData";
import { Sidebar } from "./components/layout/Sidebar";
import { Topbar } from "./components/layout/Topbar";
import { DashboardPage } from "./pages/DashboardPage";
import { ImpressorasPage } from "./pages/ImpressorasPage";
import { ManutencoesPage } from "./pages/ManutencoesPage";
import { RecargasPage } from "./pages/RecargasPage";
import { AlertasPage } from "./pages/AlertasPage";
import { RelatoriosPage } from "./pages/RelatoriosPage";
import { ConfiguracoesPage } from "./pages/ConfiguracoesPage";
import "./index.css";

export function App() {
  const [activePage, setActivePage] = useState<PageKey>("dashboard");
  const [printers, setPrinters] = useState(initialPrinters);
  const [recargas, setRecargas] = useState(initialRecargas);
  const [manutencoes, setManutencoes] = useState(initialManutencoes);
  const [alertas, setAlertas] = useState(initialAlertas);

  return (
    <div className="flex min-h-screen bg-[#f4f6fb] text-[#1d2333] font-sans antialiased">
      {/* Barra Lateral */}
      <Sidebar activePage={activePage} onSelectPage={setActivePage} />

      {/* Conteúdo Principal */}
      <div className="flex-1 flex flex-col min-w-0">
        <Topbar activePage={activePage} />

        <main className="flex-1 p-7 overflow-y-auto">
          {activePage === "dashboard" && (
            <DashboardPage
              printers={printers}
              recargas={recargas}
              alertas={alertas}
            />
          )}

          {activePage === "impressoras" && (
            <ImpressorasPage printers={printers} />
          )}

          {activePage === "manutencoes" && (
            <ManutencoesPage manutencoes={manutencoes} />
          )}

          {activePage === "recargas" && (
            <RecargasPage recargas={recargas} />
          )}

          {activePage === "alertas" && (
            <AlertasPage alertas={alertas} />
          )}

          {activePage === "relatorios" && (
            <RelatoriosPage
              printers={printers}
              recargas={recargas}
              manutencoes={manutencoes}
            />
          )}

          {activePage === "configuracoes" && <ConfiguracoesPage />}
        </main>
      </div>
    </div>
  );
}

export default App;
