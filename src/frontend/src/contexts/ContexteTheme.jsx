import { createContext, useContext, useState, useEffect } from 'react';

const ContexteTheme = createContext({
  theme: 'clair',
  basculerTheme: () => {},
});

export function FournisseurTheme({ children }) {
  const [theme, setTheme] = useState(() => {
    const themeSauvegarde = localStorage.getItem('theme_tsenantsika');
    return themeSauvegarde || 'clair';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme_tsenantsika', theme);
  }, [theme]);

  const basculerTheme = () => {
    setTheme((themeActuel) => (themeActuel === 'clair' ? 'sombre' : 'clair'));
  };

  return (
    <ContexteTheme.Provider value={{ theme, basculerTheme }}>
      {children}
    </ContexteTheme.Provider>
  );
}

export function utiliserTheme() {
  const contexte = useContext(ContexteTheme);
  if (!contexte) {
    throw new Error('utiliserTheme doit être utilisé à l\'intérieur d\'un FournisseurTheme');
  }
  return contexte;
}
// Contexte React pour la gestion globale du thème de l'application Tsenan'tsika.
// Ce contexte permet à n'importe quel composant de l'application d'accéder
// au thème actuel et de le modifier, sans avoir à faire transiter cette
// information à travers tous les composants intermédiaires.