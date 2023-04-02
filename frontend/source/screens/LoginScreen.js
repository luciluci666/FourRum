import React, { useState } from 'react';
import { StyleSheet, SafeAreaView, View, Text, Keyboard, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

import CustomInput from '../components/CustomInput'
import url from '../Globals'
import { white, light, dark, black, red } from '../Globals'

const LoginScreen = props => {
  const [username, setUsername] = useState('StolenAmigo');
  const [password, setPassword] = useState('gerllen05');

  const [errors, setErrors] = useState({})
  const handleError = (error, input) => {
    setErrors(prevState => ({...prevState, [input]: error}));
  };

  const validateUsername = () => {
    if (!username) {
      handleError('Please enter username', 'username');
    }
  };
  const validatePassword = () => {
    if (!password) {
      handleError('Please enter password', 'password');
    } else if (password.length < 8) {
      handleError('Password must be at least 8 characters long', 'password');
    }
  };
  const validate = () => {
    Keyboard.dismiss();
    setErrors({});
    let isValid = true;

    if (!username) {
      handleError('Please enter username', 'username');
      isValid = false
    }

    if (!password) {
      handleError('Please enter password', 'password');
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

    const response = await fetch(url + '/login', {
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
    <SafeAreaView style={styles.background}>
      <View style={styles.container}>
        <View style={styles.logo}>
          <Text style={styles.text}> FourRoom </Text>
        </View>
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
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  background: {
    backgroundColor: dark,
    flex: 1,
  },
  container: {
    maxWidth: 600,
    minWidth: '35%',
    alignItems: 'center',
    alignSelf: 'center',
    justifyContent: 'center',
    flex: 1,

    borderColor: light,
    borderLeftWidth: 2,
    borderRightWidth: 2
  },
  logo: {
    alignSelf: 'center',
    marginBottom: '25%',
  },
  text: {
    fontFamily: 'Montserrat-SemiBold',
    fontSize: 60,
    backgroundColor: dark,
    color: white,
  },
});
export default LoginScreen;