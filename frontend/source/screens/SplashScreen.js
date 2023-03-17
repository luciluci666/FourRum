import React, { useCallback } from 'react';
import { StyleSheet, View, Text } from 'react-native';
import { useFonts } from 'expo-font';

const SplashScreen = props => {
  const [fontsLoaded] = useFonts({
    // 'Montserrat-Light': require('../../assets/fonts/Montserrat-Light.ttf'),
    // 'Montserrat-LightItalic': require('../../assets/fonts/Montserrat-LightItalic.ttf'),
    // 'Montserrat-SemiBold': require('../../assets/fonts/Montserrat-SemiBold.ttf'),
    // 'Montserrat-SemiBoldItalic': require('../../assets/fonts/Montserrat-SemiBoldItalic.ttf'),
  });
  const onLayoutRootView = useCallback(async () => {
    if (fontsLoaded) {
      setTimeout(() => { props.navigation.navigate('Registration') }, 500);
    }
  }, [fontsLoaded]);

  if (!fontsLoaded) {
    return null;
  }

  return (
    <View style={styles.container} onLayout={onLayoutRootView}>
      <Text style={styles.text}>
        SplashScreen
      </Text>
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: 'white',
    
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    color: 'purple', 
    fontSize: 12,
    // fontFamily: 'Calibri',
  }
})

export default SplashScreen;


