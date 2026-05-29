import React from 'react';
import {
  View, Text, StyleSheet, SafeAreaView, ScrollView,
  TouchableOpacity, Alert, StatusBar
} from 'react-native';
import {
  Sprout, User, MapPin, Shield, LogOut, Calendar,
  Sparkles, TrendingUp, AlertCircle
} from 'lucide-react-native';
import { utiliserAuth } from '../contexts/ContexteAuth';
import { couleurs, espacements, rayons, tailles } from '../styles/theme';

export default function EcranAccueil() {
  const { utilisateur, deconnecter } = utiliserAuth();

  const obtenirSalutation = () => {
    const heure = new Date().getHours();
    if (heure < 12) return 'Bonjour';
    if (heure < 18) return 'Bon après-midi';
    return 'Bonsoir';
  };

  const confirmerDeconnexion = () => {
    Alert.alert(
      'Déconnexion',
      'Voulez-vous vraiment vous déconnecter ?',
      [
        { text: 'Annuler', style: 'cancel' },
        { text: 'Se déconnecter', style: 'destructive', onPress: deconnecter },
      ]
    );
  };

  const obtenirCouleurRole = (role) => {
    if (role === 'agent') return couleurs.avertissement;
    if (role === 'analyste') return couleurs.info;
    if (role === 'administrateur') return couleurs.tertiaire;
    return couleurs.succes;
  };

  return (
    <SafeAreaView style={styles.conteneur}>
      <StatusBar barStyle="light-content" backgroundColor={couleurs.primaireFoncee} />
      
      <ScrollView contentContainerStyle={styles.scrollContent}>
        
        {/* Bannière d'accueil avec dégradé vert. */}
        <View style={styles.banniere}>
          <View style={styles.logoSection}>
            <Sprout size={32} color={couleurs.texteInverse} />
            <Text style={styles.nomMarque}>Tsenan'tsika</Text>
          </View>
          
          <View style={styles.salutationSection}>
            <View style={styles.salutationLigne}>
              <Sparkles size={14} color="rgba(255, 255, 255, 0.9)" />
              <Text style={styles.salutationTexte}>
                {obtenirSalutation()}, {utilisateur?.prenoms}
              </Text>
            </View>
            <Text style={styles.bienvenue}>Bienvenue</Text>
            <Text style={styles.descriptionApp}>
              Système national de surveillance des prix alimentaires
            </Text>
          </View>
        </View>

        {/* Carte d'informations personnelles. */}
        <View style={styles.cartePerso}>
          <Text style={styles.titreCarte}>Mon profil</Text>
          
          <View style={styles.lignePerso}>
            <View style={styles.iconeLigne}>
              <User size={18} color={couleurs.primaire} />
            </View>
            <View style={styles.contenuLigne}>
              <Text style={styles.labelLigne}>Nom complet</Text>
              <Text style={styles.valeurLigne}>
                {utilisateur?.prenoms} {utilisateur?.nom}
              </Text>
            </View>
          </View>

          <View style={styles.lignePerso}>
            <View style={styles.iconeLigne}>
              <Shield size={18} color={obtenirCouleurRole(utilisateur?.role)} />
            </View>
            <View style={styles.contenuLigne}>
              <Text style={styles.labelLigne}>Rôle dans le système</Text>
              <View style={[styles.badgeRole, { backgroundColor: obtenirCouleurRole(utilisateur?.role) + '20' }]}>
                <Text style={[styles.texteBadgeRole, { color: obtenirCouleurRole(utilisateur?.role) }]}>
                  {utilisateur?.role}
                </Text>
              </View>
            </View>
          </View>

          {utilisateur?.ville_assignee_nom && (
            <View style={styles.lignePerso}>
              <View style={styles.iconeLigne}>
                <MapPin size={18} color={couleurs.secondaire} />
              </View>
              <View style={styles.contenuLigne}>
                <Text style={styles.labelLigne}>Ville d'affectation</Text>
                <Text style={styles.valeurLigne}>{utilisateur.ville_assignee_nom}</Text>
              </View>
            </View>
          )}
        </View>

        {/* Carte informative sur les fonctionnalités disponibles. */}
        <View style={styles.carteInfo}>
          <Text style={styles.titreCarte}>Vos fonctionnalités</Text>
          
          {utilisateur?.role === 'agent' && (
            <View style={styles.itemInfo}>
              <View style={styles.iconeItemInfo}>
                <TrendingUp size={20} color={couleurs.secondaire} />
              </View>
              <View style={styles.contenuItemInfo}>
                <Text style={styles.titreItemInfo}>Saisie de prix</Text>
                <Text style={styles.descriptionItemInfo}>
                  Soumettez les prix observés sur les marchés depuis l'onglet Saisie.
                </Text>
              </View>
            </View>
          )}

          <View style={styles.itemInfo}>
            <View style={styles.iconeItemInfo}>
              <AlertCircle size={20} color={couleurs.erreur} />
            </View>
            <View style={styles.contenuItemInfo}>
              <Text style={styles.titreItemInfo}>Tableau de bord</Text>
              <Text style={styles.descriptionItemInfo}>
                Consultez les alertes actives et le classement des hausses de prix.
              </Text>
            </View>
          </View>
        </View>

        {/* Bouton de déconnexion. */}
        <TouchableOpacity
          style={styles.boutonDeconnexion}
          onPress={confirmerDeconnexion}
          activeOpacity={0.8}
        >
          <LogOut size={20} color={couleurs.erreur} />
          <Text style={styles.texteDeconnexion}>Se déconnecter</Text>
        </TouchableOpacity>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  conteneur: {
    flex: 1,
    backgroundColor: couleurs.fond,
  },
  scrollContent: {
    paddingBottom: espacements.xl,
  },
  banniere: {
    backgroundColor: couleurs.primaire,
    padding: espacements.lg,
    paddingTop: espacements.xl,
    paddingBottom: espacements.xxl,
    borderBottomLeftRadius: rayons.xl,
    borderBottomRightRadius: rayons.xl,
  },
  logoSection: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.sm,
    marginBottom: espacements.lg,
  },
  nomMarque: {
    fontSize: tailles.texteLg,
    fontWeight: '700',
    color: couleurs.texteInverse,
  },
  salutationSection: {
    marginTop: espacements.sm,
  },
  salutationLigne: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: espacements.xs,
    marginBottom: espacements.sm,
  },
  salutationTexte: {
    color: 'rgba(255, 255, 255, 0.9)',
    fontSize: tailles.texteBase,
  },
  bienvenue: {
    fontSize: tailles.texteGrand,
    fontWeight: '800',
    color: couleurs.texteInverse,
    marginBottom: espacements.xs,
  },
  descriptionApp: {
    fontSize: tailles.texteBase,
    color: 'rgba(255, 255, 255, 0.9)',
    lineHeight: 22,
  },
  cartePerso: {
    backgroundColor: couleurs.fondSecondaire,
    marginHorizontal: espacements.lg,
    marginTop: -espacements.lg,
    padding: espacements.lg,
    borderRadius: rayons.lg,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  titreCarte: {
    fontSize: tailles.texteLg,
    fontWeight: '700',
    color: couleurs.textePrincipal,
    marginBottom: espacements.md,
  },
  lignePerso: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: espacements.sm,
  },
  iconeLigne: {
    width: 40,
    height: 40,
    borderRadius: rayons.md,
    backgroundColor: couleurs.fond,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: espacements.md,
  },
  contenuLigne: {
    flex: 1,
  },
  labelLigne: {
    fontSize: tailles.texteSm,
    color: couleurs.texteDiscret,
    marginBottom: 2,
  },
  valeurLigne: {
    fontSize: tailles.texteBase,
    fontWeight: '600',
    color: couleurs.textePrincipal,
  },
  badgeRole: {
    alignSelf: 'flex-start',
    paddingHorizontal: espacements.md,
    paddingVertical: 4,
    borderRadius: rayons.full,
  },
  texteBadgeRole: {
    fontSize: tailles.texteSm,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  carteInfo: {
    backgroundColor: couleurs.fondSecondaire,
    marginHorizontal: espacements.lg,
    marginTop: espacements.md,
    padding: espacements.lg,
    borderRadius: rayons.lg,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  itemInfo: {
    flexDirection: 'row',
    paddingVertical: espacements.sm,
  },
  iconeItemInfo: {
    width: 40,
    height: 40,
    borderRadius: rayons.md,
    backgroundColor: couleurs.fond,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: espacements.md,
  },
  contenuItemInfo: {
    flex: 1,
  },
  titreItemInfo: {
    fontSize: tailles.texteBase,
    fontWeight: '600',
    color: couleurs.textePrincipal,
    marginBottom: 2,
  },
  descriptionItemInfo: {
    fontSize: tailles.texteSm,
    color: couleurs.texteDiscret,
    lineHeight: 18,
  },
  boutonDeconnexion: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: couleurs.fondSecondaire,
    marginHorizontal: espacements.lg,
    marginTop: espacements.lg,
    paddingVertical: espacements.md,
    borderRadius: rayons.md,
    borderWidth: 1,
    borderColor: couleurs.erreur,
    gap: espacements.sm,
  },
  texteDeconnexion: {
    fontSize: tailles.texteBase,
    fontWeight: '600',
    color: couleurs.erreur,
  },
});