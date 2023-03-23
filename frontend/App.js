import React, { useState, useEffect, useCallback } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';
import { useFonts } from 'expo-font';
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
// import * as SplashScreen from 'expo-splash-screen';

import RegistrationScreen from './source/screens/RegistrationScreen'
import SplashScreen from './source/screens/SplashScreen';
import LoginScreen from './source/screens/LoginScreen';
import HomeScreen from './source/screens/HomeScreen';

// SplashScreen.preventAutoHideAsync();
const Stack = createStackNavigator();

export default function App() {
  // const [fontsLoaded] = useFonts({
  //   'Montserrat-Light': require('./assets/fonts/Montserrat-Light.ttf'),
  //   'Montserrat-LightItalic': require('./assets/fonts/Montserrat-LightItalic.ttf'),
  //   'Montserrat-SemiBold': require('./assets/fonts/Montserrat-SemiBold.ttf'),
  //   'Montserrat-SemiBoldItalic': require('./assets/fonts/Montserrat-SemiBoldItalic.ttf'),
  // });

  // const onLayoutRootView = useCallback(async () => {
  //   if (fontsLoaded) {
  //     await SplashScreen.hideAsync();
  //   }
  // }, [fontsLoaded]);

  // if (!fontsLoaded) {
  //   return null;
  // }

  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Loading"
          component={SplashScreen}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen 
          name="Registration"
          component={RegistrationScreen}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen 
          name="Log in"
          component={LoginScreen}
          options={{
            headerShown: false,
          }}
        />
        <Stack.Screen 
          name="Home"
          component={HomeScreen}
          options={{
            headerShown: false,
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

const styles = StyleSheet.create({
  container: {
    width: '70%',
    maxWidth: 300,
    height: '30%',
    maxHeight: 180,
  },
  text: {
    fontFamily: 'mt-bold-italic',
  }
});
