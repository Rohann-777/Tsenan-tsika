import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { FournisseurAuth } from './src/contexts/ContexteAuth';
import NavigateurPrincipal from './src/components/NavigateurPrincipal';

export default function App() {
  return (
    <SafeAreaProvider>
      <FournisseurAuth>
        <NavigateurPrincipal />
        <StatusBar style="auto" />
      </FournisseurAuth>
    </SafeAreaProvider>
  );
}