import React, { useState } from 'react';
import { StyleSheet, View, SafeAreaView, Keyboard, Button, Text } from 'react-native';
import {getLocales} from "react-native-localize";

import CustomInput from '../components/CustomInput'
import url from '../Globals'
import { white, light, dark, black, red } from '../Globals'

const RegistrationScreen = props => {
  const [username, setUsername] = useState('StolenAmigo');
  const [email, setEmail] = useState('gerllen05@gmail.com');
  const [password, setPassword] = useState('gerllen05');
  const [confirmPassword, setConfirmPassword] = useState('gerllen05');

  const [errors, setErrors] = useState({})
  const handleError = (error, input) => {
    setErrors(prevState => ({...prevState, [input]: error}));
  };

  const validateUsername = () => {
    if (!username) {
      handleError('Please enter username', 'username');
    }
  };
  const validateEmail = () => {
    if (!email) {
      handleError('Please enter email', 'email');
    } else if (!email.match(/\S+@\S+\.\S+/)) {
      handleError('Please enter a valid email', 'email');
    }
  };
  const validatePassword = () => {
    if (!password) {
      handleError('Please enter password', 'password');
    } else if (password.length < 8) {
      handleError('Password must be at least 8 characters long', 'password');
    }
  };
  const validateConfirmPassword = () => {
    if (!confirmPassword) {
      handleError('Please confirm password', 'confirmPassword');
    } else if (confirmPassword != password) {
      handleError('This password does not match the previous one', 'confirmPassword');
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

    if (!email) {
      handleError('Please enter email', 'email');
      isValid = false
    } else if (!email.match(/\S+@\S+\.\S+/)) {
      handleError('Please enter a valid email', 'email');
      isValid = false
    }

    if (!password) {
      handleError('Please enter password', 'password');
      isValid = false
    } else if (password.length < 8) {
      handleError('Password must be at least 8 characters long', 'password');
      isValid = false
    }

    if (!confirmPassword) {
      handleError('Please confirm password', 'confirmPassword');
      isValid = false
    } else if (confirmPassword != password) {
      handleError('This password does not match the previous one', 'confirmPassword');
      isValid = false
    }

    if (isValid) {
      console.log('Trying to register...');
      registration();
    }
  };

  const registration = async () => {
    let langCode = "en";
    try {
      langCode = getLocales()[0].languageCode;
    } catch (error) {
      console.warn(error);
    } 
    let body = {
      "username": username,
      "email": email,
      "password": password,
      "locale": langCode,
    };
    console.log(body);

    const response = await fetch(url + '/reg', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      });
    response.json().then(data => {
        if (!response.ok) {
          console.log(data.detail);
        } else {
          console.log(data)
          props.navigation.navigate('Log in')
        }
      });
  };

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
        value={email}
        setValue={setEmail}
        placeholder="Enter email"
        error={errors.email}
        errorHandler={() => handleError(null, 'email')}
        validate={validateEmail} />
        <CustomInput
        value={password}
        setValue={setPassword}
        placeholder="Enter password"
        error={errors.password}
        errorHandler={() => handleError(null, 'password')}
        validate={validatePassword}
        secureTextEntry />
        <CustomInput
        value={confirmPassword}
        setValue={setConfirmPassword}
        placeholder="Confirm password"
        error={errors.confirmPassword}
        errorHandler={() => handleError(null, 'confirmPassword')}
        validate={validateConfirmPassword}
        secureTextEntry />
        <Button 
        title="Submit" 
        onPress = {validate}/>
        <Button 
        title="Log in" 
        onPress = {() => props.navigation.navigate('Log in')}/>
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

export default RegistrationScreen;