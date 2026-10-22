export type PrinterStatus = "excelente" | "bom" | "ruim" | "critico";

export interface Printer {
  id: number;
  nome: string;
  local: string;
  status: PrinterStatus;
  insumo: string;
  nivel: number;
  modelo: string;
  setor: string;
  previsao: string;
  ultimaRecarga: string;
  ultimaManutencao: string;
  ultimaVerificacao: string;
}

export interface Recarga {
  id: number;
  nome: string;
  data: string;
  tipo: string;
  insumo: string;
}

export interface Manutencao {
  id: number;
  nome: string;
  tipo: "Preventiva" | "Corretiva" | string;
  data: string;
  tecnico: string;
  status: "Agendada" | "Em andamento" | "Concluída" | string;
}

export interface Alerta {
  tipo: PrinterStatus;
  texto: string;
  tempo: string;
}

export type PageKey =
  | "dashboard"
  | "impressoras"
  | "manutencoes"
  | "recargas"
  | "alertas"
  | "relatorios"
  | "configuracoes";
