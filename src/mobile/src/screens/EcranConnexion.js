import React, { useState } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, StyleSheet,
  KeyboardAvoidingView, Platform, ScrollView, Alert,
  ActivityIndicator, StatusBar
} from 'react-native';
import { Sprout, Mail, Lock, LogIn, AlertCircle } from 'lucide-react-native';
import { utiliserAuth } from '../contexts/ContexteAuth';
import { couleurs, espacements, rayons, tailles } from '../styles/theme';

export default function EcranConnexion() {
  const { connecter } = utiliserAuth();
  const [email, setEmail] = useState('');
  const [motDePasse, setMotDePasse] = useState('');
  const [chargement, setChargement] = useState(false);
  const [erreur, setErreur] = useState(null);

  const gererConnexion = async () => {
    if (!email || !motDePasse) {
      setErreur('Veuillez remplir tous les champs');
      return;
    }
    
    setChargement(true);
    setErreur(null);
    
    try {
      await connecter(email, motDePasse);
    } catch (err) {
      if (err.response && err.response.status === 401) {
        setErreur('Email ou mot de passe incorrect');
      } else if (err.response && err.response.status === 403) {
        setErreur(err.response.data.detail || 'Ce compte a été désactivé');
      } else {
        setErreur('Impossible de se connecter au serveur');
      }
      console.error('Erreur de connexion:', err);
    } finally {
      setChargement(false);
    }
  };

  return (
    <View style={styles.conteneur}>
      <StatusBar barStyle="light-content" backgroundColor={couleurs.primaireFoncee} />
      
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.kav}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContent}
          keyboardShouldPersistTaps="handled"
        >
          
          {/* Section d'en-tête avec logo et identité de l'application. */}
          <View style={styles.entete}>
            <View style={styles.logoConteneur}>
              <Sprout size={48} color={couleurs.texteInverse} />
            </View>
            <Text style={styles.nomApp}>Tsenan'tsika</Text>
            <Text style={styles.sousTitreApp}>
              Surveillance des prix alimentaires
            </Text>
          </View>

          {/* Carte du formulaire de connexion. */}
          <View style={styles.carteFormulaire}>
            <Text style={styles.titreFormulaire}>Connexion</Text>
            <Text style={styles.descriptionFormulaire}>
              Accédez à votre espace personnel
            </Text>

            {erreur && (
              <View style={styles.boiteErreur}>
                <AlertCircle size={18} color={couleurs.erreurTexte} />
                <Text style={styles.texteErreur}>{erreur}</Text>
              </View>
            )}

            <View style={styles.groupeChamp}>
              <Text style={styles.label}>Adresse email</Text>
              <View style={styles.conteneurInput}>
                <Mail size={18} color={couleurs.texteDiscret} style={styles.iconeInput} />
                <TextInput
                  style={styles.input}
                  placeholder="exemple@tsenantsika.mg"
                  placeholderTextColor={couleurs.texteDiscret}
                  value={email}
                  onChangeText={setEmail}
                  autoCapitalize="none"
                  keyboardType="email-address"
                  autoCorrect={false}
                  editable={!chargement}
                />
              </View>
            </View>

            <View style={styles.groupeChamp}>
              <Text style={styles.label}>Mot de passe</Text>
              <View style={styles.conteneurInput}>
                <Lock size={18} color={couleurs.texteDiscret} style={styles.iconeInput} />
                <TextInput
                  style={styles.input}
                  placeholder="Votre mot de passe"
                  placeholderTextColor={couleurs.texteDiscret}
                  value={motDePasse}
                  onChangeText={setMotDePasse}
                  secureTextEntry
                  editable={!chargement}
                />
              </View>
            </View>

            <TouchableOpacity
              style={[styles.boutonConnexion, chargement && styles.boutonDesactive]}
              onPress={gererConnexion}
              disabled={chargement}
              activeOpacity={0.8}
            >
              {chargement ? (
                <ActivityIndicator color={couleurs.texteInverse} />
              ) : (
                <>
                  <LogIn size={20} color={couleurs.texteInverse} />
                  <Text style={styles.texteBoutonConnexion}>Se connecter</Text>
                </>
              )}
            </TouchableOpacity>
          </View>

          {/* Pied de page avec mention. */}
          <View style={styles.piedPage}>
            <Text style={styles.textePiedPage}>
              Projet transversal L2 — ESMIA Innovation
            </Text>
          </View>

        </ScrollView>
      </KeyboardAvoidingView>
    </View>
  );
}

const styles = StyleSheet.create({
  conteneur: {
    flex: 1,
    backgroundColor: couleurs.primaire,
  },
  kav: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingVertical: espacements.xl,
  },
  entete: {
    alignItems: 'center',
    paddingHorizontal: espacements.lg,
    marginBottom: espacements.xl,
  },
  logoConteneur: {
    width: 80,
    height: 80,
    borderRadius: rayons.xl,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: espacements.md,
    borderWidth: 2,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  nomApp: {
    fontSize: tailles.texteGrand,
    fontWeight: '800',
    color: couleurs.texteInverse,
    marginBottom: espacements.xs,
    letterSpacing: -0.5,
  },
  sousTitreApp: {
    fontSize: tailles.texteBase,
    color: 'rgba(255, 255, 255, 0.9)',
    textAlign: 'center',
  },
  carteFormulaire: {
    backgroundColor: couleurs.fondSecondaire,
    marginHorizontal: espacements.lg,
    padding: espacements.lg,
    borderRadius: rayons.xl,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 8,
  },
  titreFormulaire: {
    fontSize: tailles.texteXl,
    fontWeight: '700',
    color: couleurs.textePrincipal,
    marginBottom: espacements.xs,
  },
  descriptionFormulaire: {
    fontSize: tailles.texteBase,
    color: couleurs.texteDiscret,
    marginBottom: espacements.lg,
  },
  boiteErreur: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: couleurs.erreurFond,
    borderLeftWidth: 4,
    borderLeftColor: couleurs.erreur,
    padding: espacements.md,
    borderRadius: rayons.md,
    marginBottom: espacements.md,
    gap: espacements.sm,
  },
  texteErreur: {
    flex: 1,
    color: couleurs.erreurTexte,
    fontSize: tailles.texteSm,
  },
  groupeChamp: {
    marginBottom: espacements.md,
  },
  label: {
    fontSize: tailles.texteSm,
    fontWeight: '600',
    color: couleurs.texteSecondaire,
    marginBottom: espacements.sm,
  },
  conteneurInput: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: couleurs.fond,
    borderWidth: 2,
    borderColor: couleurs.bordure,
    borderRadius: rayons.md,
    paddingHorizontal: espacements.md,
  },
  iconeInput: {
    marginRight: espacements.sm,
  },
  input: {
    flex: 1,
    paddingVertical: espacements.md,
    fontSize: tailles.texteBase,
    color: couleurs.textePrincipal,
  },
  boutonConnexion: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: couleurs.primaire,
    paddingVertical: espacements.md,
    borderRadius: rayons.md,
    marginTop: espacements.md,
    gap: espacements.sm,
    shadowColor: couleurs.primaireFoncee,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  boutonDesactive: {
    opacity: 0.7,
  },
  texteBoutonConnexion: {
    color: couleurs.texteInverse,
    fontSize: tailles.texteBase,
    fontWeight: '600',
  },
  piedPage: {
    alignItems: 'center',
    paddingHorizontal: espacements.lg,
    marginTop: espacements.xl,
  },
  textePiedPage: {
    fontSize: tailles.texteFin,
    color: 'rgba(255, 255, 255, 0.7)',
    textAlign: 'center',
  },
});