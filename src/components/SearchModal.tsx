import React, { useState, useEffect, useRef } from 'react';

interface DocSection {
  title: string;
  content: string;
}

interface DocItem {
  id: string;
  title: string;
  description: string;
  icon: string;
  sections?: DocSection[];
}

interface SearchModalProps {
  docs: DocItem[];
}

export default function SearchModal({ docs }: SearchModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      } else if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery('');
    }
  }, [isOpen]);

  useEffect(() => {
    const handleOpenSearch = () => setIsOpen(true);
    window.addEventListener('open-search-modal', handleOpenSearch);
    return () => window.removeEventListener('open-search-modal', handleOpenSearch);
  }, []);

  const results = query.trim() === '' ? [] : docs.flatMap((doc) => {
    const docMatches = doc.title.toLowerCase().includes(query.toLowerCase()) || 
                       doc.description.toLowerCase().includes(query.toLowerCase());
    
    const matchingSections = (doc.sections || []).filter(
      (sec) => sec.title.toLowerCase().includes(query.toLowerCase()) ||
               sec.content.toLowerCase().includes(query.toLowerCase())
    );

    const res = [];
    if (docMatches) {
      res.push({
        id: doc.id,
        title: doc.title,
        subtitle: doc.description,
        icon: doc.icon,
        href: `/${doc.id}`,
      });
    }

    matchingSections.forEach((sec) => {
      res.push({
        id: `${doc.id}-${sec.title}`,
        title: `${doc.title} › ${sec.title}`,
        subtitle: sec.content.slice(0, 100) + '...',
        icon: doc.icon,
        href: `/${doc.id}#${encodeURIComponent(sec.title.toLowerCase().replace(/\s+/g, '-'))}`,
      });
    });

    return res;
  });

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-16 sm:pt-24 px-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div className="fixed inset-0" onClick={() => setIsOpen(false)} />

      <div className="relative w-full max-w-2xl bg-white rounded-2xl shadow-2xl border border-slate-200/80 overflow-hidden z-10 flex flex-col max-h-[80vh]">
        <div className="flex items-center px-4 py-3.5 border-b border-slate-100 bg-slate-50/50">
          <svg className="w-5 h-5 text-blue-600 mr-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            ref={inputRef}
            type="text"
            className="w-full bg-transparent text-slate-900 placeholder-slate-400 text-base focus:outline-none"
            placeholder="Buscar documentos, guías, preguntas..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            onClick={() => setIsOpen(false)}
            className="ml-2 text-xs font-semibold px-2 py-1 bg-slate-200 text-slate-600 rounded-md hover:bg-slate-300 transition-colors"
          >
            ESC
          </button>
        </div>

        <div className="overflow-y-auto p-3 flex-1">
          {query.trim() === '' ? (
            <div className="text-center py-10 px-4 text-slate-400">
              <p className="text-sm font-medium">Escribe algo para buscar en la documentación...</p>
              <div className="mt-4 flex justify-center gap-2 flex-wrap">
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-600 border border-blue-100">
                  Reglamento
                </span>
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-600 border border-emerald-100">
                  Becas
                </span>
                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-50 text-indigo-600 border border-indigo-100">
                  Reembolsos
                </span>
              </div>
            </div>
          ) : results.length === 0 ? (
            <div className="text-center py-12 px-4 text-slate-500">
              <p className="text-base font-semibold">No se encontraron resultados</p>
              <p className="text-xs mt-1 text-slate-400">Intenta con otros términos como &quot;certificado&quot; o &quot;inscripción&quot;</p>
            </div>
          ) : (
            <div className="space-y-1">
              {results.map((item) => (
                <a
                  key={item.id}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className="flex items-start gap-3 p-3 rounded-xl hover:bg-blue-50/80 transition-colors group"
                >
                  <span className="text-xl p-2 rounded-lg bg-slate-100 group-hover:bg-blue-100 transition-colors shrink-0">
                    {item.icon}
                  </span>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-slate-900 group-hover:text-blue-600 transition-colors truncate">
                      {item.title}
                    </div>
                    <div className="text-xs text-slate-500 line-clamp-1 mt-0.5">
                      {item.subtitle}
                    </div>
                  </div>
                  <svg className="w-4 h-4 text-slate-400 group-hover:text-blue-600 shrink-0 self-center opacity-0 group-hover:opacity-100 transition-all -translate-x-1 group-hover:translate-x-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="9 5l7 7-7 7" />
                  </svg>
                </a>
              ))}
            </div>
          )}
        </div>

        <div className="px-4 py-2.5 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center gap-2">
            <span className="px-1.5 py-0.5 bg-white rounded border border-slate-200 font-mono text-[10px]">↑↓</span>
            <span>Navegar</span>
            <span className="px-1.5 py-0.5 bg-white rounded border border-slate-200 font-mono text-[10px] ml-2">↵</span>
            <span>Seleccionar</span>
          </div>
          <span>AprendeYa Docs</span>
        </div>
      </div>
    </div>
  );
}
