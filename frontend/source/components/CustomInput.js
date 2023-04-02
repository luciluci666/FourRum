import React, {useState} from 'react';
import { TextInput } from 'react-native';
import { StyleSheet, Text, View } from 'react-native';

import { white, light, dark, black, red } from '../Globals'

const CustomInput = ({ value, setValue = () => {}, placeholder, error, errorHandler = () => {}, validate = () => {}, secureTextEntry }) => {
  const [isFocused, setIsFocused] = React.useState(false);

  return (
    <View style={styles.container} >
      <View style={
        [{borderColor: error
          ? red
          : isFocused
          ? white
          : light , }, styles.box]} >
        <TextInput 
        style={styles.input} 
        value={value}
        onChangeText={setValue}
        onFocus={() => {errorHandler(), setIsFocused(true)}}
        onBlur={() => {validate(), setIsFocused(false)}}
        placeholder={placeholder}
        autoCorrect={false}
        secureTextEntry={secureTextEntry} />
      </View>
      
      {error && (
      <Text style={styles.error}>
        {error}
      </Text> )}
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    width: '70%',
    maxWidth: 400,
    height: "10%",
    maxHeight: 50,
    marginVertical: 5,
    marginHorizontal: 5,
    borderRadius: 5,
  },
  box: {
    height: "80%",
    borderRadius: 5,
    borderWidth: 2,
    backgroundColor: dark,
  },
  input: {
    width: '100%',
    height: "100%",
    marginHorizontal: 3,
    outlineStyle: 'none',
    color: white,
  },
  error: {
    fontSize: 12,
    backgroundColor: dark,
    color: red,
  }
})

export default CustomInput;