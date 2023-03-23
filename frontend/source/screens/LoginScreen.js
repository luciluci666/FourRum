import React, { useState } from 'react';
import { StyleSheet, SafeAreaView, Keyboard, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import CustomInput from '../components/CustomInput'
import url from '../Globals'

const LoginScreen = props => {
  const [username, setUsername] = useState('StolenAmigo');
  const [password, setPassword] = useState('gerllen05');

  const [errors, setErrors] = useState({})
  const handleError = (error, input) => {
    setErrors(prevState => ({...prevState, [input]: error}));
  };

  const validateUsername = () => {
    if (!username) {
      handleError('Please input username', 'username');
    }
  };
  const validatePassword = () => {
    if (!password) {
      handleError('Please input password', 'password');
    } else if (password.length < 8) {
      handleError('Password must be at least 8 characters long', 'password');
    }
  };
  const validate = () => {
    Keyboard.dismiss();
    setErrors({});
    let isValid = true;

    if (!username) {
      handleError('Please input username', 'username');
      isValid = false
    }

    if (!password) {
      handleError('Please input password', 'password');
      isValid = false
    } else if (password.length < 8) {
      handleError('Password must be at least 8 characters long', 'password');
      isValid = false
    }

    if (isValid) {
      console.log('Trying to log in...');
      login();
    }
  };

  const login = async () => {
    let body = {
      "username": username,
      "password": password,
    };

    const response = await fetch(url + '/user/login/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      });
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
  };

  const storeUserData = async (value) => {
    try {
      await AsyncStorage.setItem('FourRoomUserData', value)
    } catch (e) {
      console.warn(e)
    }
  }

  return (
    <SafeAreaView style={styles.container}>
      <CustomInput
      value={username}
      setValue={setUsername}
      placeholder="Enter your future username"
      error={errors.username}
      errorHandler={() => handleError(null, 'username')}
      validate={validateUsername} />
      <CustomInput
      value={password}
      setValue={setPassword}
      placeholder="Enter password"
      error={errors.password}
      errorHandler={() => handleError(null, 'password')}
      validate={validatePassword}
      secureTextEntry />
      <Button 
      title="Submit" 
      onPress = {validate}/>
      <Button 
      title="Register" 
      onPress = {() => props.navigation.navigate('Registration')}/>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#94B5E1',
    alignItems: 'center'
  },
});

export default LoginScreen;