import { ChevronRight, Menu } from "lucide-react";
import { useState } from "react";

const navItems = [
  { href: "#visao", label: "Visao" },
  { href: "#fluxo", label: "Fluxo" },
  { href: "#api", label: "API" },
  { href: "#ranking", label: "Ranking" },
  { href: "#avaliacao", label: "Avaliacao" },
  { href: "#limites", label: "Limites" },
];

interface AppShellProps {
  children: React.ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  const [open, setOpen] = useState(false);

  return (
    <div className="app-shell">
      <a className="skip-link" href="#conteudo">
        Ir para o conteudo
      </a>

      <header className="topbar" aria-label="Navegacao principal">
        <a className="brand" href="#topo" aria-label="Kouzina Reco">
          <span className="brand__mark">KR</span>
          <span>
            <strong>Kouzina Reco</strong>
            <small>Frontend visual</small>
          </span>
        </a>

        <button
          className="menu-button"
          type="button"
          aria-label="Abrir menu de secoes"
          aria-expanded={open}
          onClick={() => setOpen((value) => !value)}
        >
          <Menu aria-hidden="true" size={20} />
        </button>

        <nav className={`nav ${open ? "is-open" : ""}`} aria-label="Secoes">
          {navItems.map((item) => (
            <a key={item.href} href={item.href} onClick={() => setOpen(false)}>
              {item.label}
              <ChevronRight aria-hidden="true" size={14} />
            </a>
          ))}
        </nav>
      </header>

      <main id="conteudo">{children}</main>
    </div>
  );
}
