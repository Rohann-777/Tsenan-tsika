import React from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Home, LayoutDashboard, PlusCircle } from 'lucide-react-native';
import { utiliserAuth } from '../contexts/ContexteAuth';
import { couleurs, espacements } from '../styles/theme';
import EcranConnexion from '../screens/EcranConnexion';
import EcranAccueil from '../screens/EcranAccueil';
import EcranTableauBord from '../screens/EcranTableauBord';
import EcranSaisiePrix from '../screens/EcranSaisiePrix';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function NavigateurOnglets() {
  const { utilisateur } = utiliserAuth();
  const estAgent = utilisateur?.role === 'agent';

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: couleurs.primaire,
        tabBarInactiveTintColor: couleurs.texteDiscret,
        tabBarStyle: {
          backgroundColor: couleurs.fondSecondaire,
          borderTopColor: couleurs.bordure,
          borderTopWidth: 1,
          paddingTop: espacements.xs,
          paddingBottom: espacements.sm,
          height: 70,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
          marginTop: 4,
        },
      }}
    >
      <Tab.Screen
        name="Accueil"
        component={EcranAccueil}
        options={{
          tabBarIcon: ({ color, size }) => <Home size={size} color={color} />,
        }}
      />
      
      <Tab.Screen
        name="Tableau de bord"
        component={EcranTableauBord}
        options={{
          tabBarIcon: ({ color, size }) => <LayoutDashboard size={size} color={color} />,
        }}
      />
      
      {/* L'onglet Saisie n'est visible que pour les agents. */}
      {estAgent && (
        <Tab.Screen
          name="Saisie"
          component={EcranSaisiePrix}
          options={{
            tabBarIcon: ({ color, size }) => <PlusCircle size={size} color={color} />,
          }}
        />
      )}
    </Tab.Navigator>
  );
}

export default function NavigateurPrincipal() {
  const { utilisateur, chargement } = utiliserAuth();

  if (chargement) {
    return (
      <View style={styles.conteneurChargement}>
        <ActivityIndicator size="large" color={couleurs.primaire} />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {utilisateur ? (
          <Stack.Screen name="Principal" component={NavigateurOnglets} />
        ) : (
          <Stack.Screen name="Connexion" component={EcranConnexion} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  conteneurChargement: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: couleurs.fond,
  },
});