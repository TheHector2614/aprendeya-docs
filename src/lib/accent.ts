/**
 * Paleta de acento por documento.
 *
 * Tailwind analiza el código fuente en busca de nombres de clase literales, así
 * que las clases se escriben completas aquí en lugar de interpolarse
 * (`bg-${color}-50` no se generaría nunca).
 */
export interface AccentClasses {
  headerGradient: string
  glow: string
  badge: string
}

const ACCENTS: Record<string, AccentClasses> = {
  blue: {
    headerGradient: "bg-gradient-to-br from-white via-slate-50 to-blue-50/50",
    glow: "bg-blue-500/10",
    badge: "bg-blue-50 text-blue-600 border-blue-100",
  },
  emerald: {
    headerGradient: "bg-gradient-to-br from-white via-slate-50 to-emerald-50/50",
    glow: "bg-emerald-500/10",
    badge: "bg-emerald-50 text-emerald-600 border-emerald-100",
  },
  indigo: {
    headerGradient: "bg-gradient-to-br from-white via-slate-50 to-indigo-50/50",
    glow: "bg-indigo-500/10",
    badge: "bg-indigo-50 text-indigo-600 border-indigo-100",
  },
}

export type AccentName = keyof typeof ACCENTS

export function getAccent(name: string | undefined): AccentClasses {
  return ACCENTS[name ?? "blue"] ?? ACCENTS.blue
}
