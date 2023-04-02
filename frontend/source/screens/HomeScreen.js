import React, { useEffect, useState } from 'react';
import { StyleSheet, SafeAreaView, Text, Keyboard, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import url from '../Globals'
import { white, light, dark, black, red } from '../Globals'

const HomeScreen = props => {
  const [accessToken, setAccessToken] = useState('');
  const [userRooms, setUserRooms] = useState([]);

  useEffect(() => {
    if (!accessToken) {
    getUserData();
    }
    else {
    fetchUserRooms();
    }
    return () => {};
  }, [accessToken]);

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
    const response = await fetch(url + '/user/rooms/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'token': `${accessToken}`
      },
    })
    response.json().then(async (data) => {
        if (!response.ok) {
          console.log(data.detail);
        } else {
          console.log(data);
          setUserRooms(data.rooms)
        }
      });
  }

  return (
    <SafeAreaView style={styles.container}>
      <Text>
      {userRooms}
      </Text>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: dark,
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
  },
});

export default HomeScreen;