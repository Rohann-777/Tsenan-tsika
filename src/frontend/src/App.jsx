import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import PageGestionUtilisateurs from './pages/PageGestionUtilisateurs';
import PageConnexion from './pages/PageConnexion';
import PageInscription from './pages/PageInscription';
import PageAccueil from './pages/PageAccueil';
import PageTableauBord from './pages/PageTableauBord';
import PageSaisiePrix from './pages/PageSaisiePrix';
import PageItineraire from './pages/PageItineraire';
import PageSurveillanceDoublons from './pages/PageSurveillanceDoublons';
import MisePage from './components/MisePage';
import { serviceAuth } from './services/api';
import './styles/App.css';
function RouteProtegee({ children, rolesAutorises }) {
  const estConnecte = serviceAuth.estConnecte();
  const utilisateur = serviceAuth.obtenirUtilisateurConnecte();
  
  if (!estConnecte) {
    return <Navigate to="/connexion" replace />;
  }
  
  if (rolesAutorises && !rolesAutorises.includes(utilisateur.role)) {
    // Redirection vers la page principale selon le rôle de l'utilisateur
    const pageParDefaut = obtenirPagePrincipale(utilisateur.role);
    return <Navigate to={pageParDefaut} replace />;
  }
  
  return <MisePage>{children}</MisePage>;
}

function obtenirPagePrincipale(role) {
  if (role === 'agent') {
    return '/saisie';
  }
  if (role === 'analyste' || role === 'administrateur' || role === 'citoyen') {
    return '/tableau-bord';
  }
  return '/connexion';
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Routes publiques sans mise en page partagée. */}
        <Route path="/connexion" element={<PageConnexion />} />
        <Route path="/inscription" element={<PageInscription />} />
        
        {/* Routes protégées avec mise en page partagée automatique. */}
        <Route
          path="/"
          element={
            <RouteProtegee>
              <PageAccueil />
            </RouteProtegee>
          }
        />
        
        <Route
          path="/tableau-bord"
          element={
            <RouteProtegee>
              <PageTableauBord />
            </RouteProtegee>
          }
        />
        
        <Route
          path="/saisie"
          element={
            <RouteProtegee rolesAutorises={['agent']}>
              <PageSaisiePrix />
            </RouteProtegee>
          }
        />
        
        <Route
          path="/itineraire"
          element={
            <RouteProtegee rolesAutorises={['analyste']}>
              <PageItineraire />
            </RouteProtegee>
          }
        />

        <Route
          path="/admin/utilisateurs"
          element={
            <RouteProtegee rolesAutorises={['administrateur']}>
              <PageGestionUtilisateurs />
            </RouteProtegee>
          }
        />

        <Route
          path="/admin/doublons"
          element={
            <RouteProtegee rolesAutorises={['administrateur']}>
              <PageSurveillanceDoublons />
            </RouteProtegee>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;