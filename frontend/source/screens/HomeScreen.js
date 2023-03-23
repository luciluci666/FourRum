import React, { useEffect, useState } from 'react';
import { StyleSheet, SafeAreaView, Text, Keyboard, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import url from '../Globals'

const HomeScreen = props => {
  const [accessToken, setAccessToken] = useState('');
  useEffect(() => {
    getUserData();
    return () => {};
  }, []);

  const getUserData = async () => {
    try {
      const value = await AsyncStorage.getItem('FourRoomUserData');
      if(value !== null) {
        console.log(value);
        setAccessToken(value);
      };
    } catch(e) {
      console.warn(e)
    };
  };

  const fetchUserRooms = async () => {
    const response = await fetch(url + '/user/login/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Authorization': `${accessToken}`
      },
    })
    response.json().then(async (data) => {
        if (!response.ok) {
          console.log(data.detail);
        } else {
          console.log(data);
          const jwt = data.access_token;
          await storeUserData(jwt);
          props.navigation.navigate('Home');
        }
      });
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text>
        {accessToken}
        1234
      </Text>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#94B5E1',
    alignItems: 'center'
  },
});

export default HomeScreen;