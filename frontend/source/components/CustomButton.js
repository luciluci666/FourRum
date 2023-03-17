import React, {useState} from 'react';
import { TextInput } from 'react-native';
import { StyleSheet, Text, View } from 'react-native';

const CustomButton = ({ value, setValue = () => {}, placeholder, error, errorHandler = () => {}, validate = () => {}, secureTextEntry }) => {
  const [isFocused, setIsFocused] = React.useState(false);

  return (
    <View style={styles.container} >
      <View style={
        {borderColor: error
          ? 'red'
          : isFocused
          ? 'green'
          : 'blue' ,
        borderWidth: 1 } } >
        <TextInput 
        style={styles.input} 
        value={value}
        onChangeText={setValue}
        onFocus={() => {errorHandler(), setIsFocused(true)}}
        onBlur={() => {validate(), setIsFocused(false)}}
        placeholder={placeholder}
        autoCorrect={false}
        secureTextEntry={secureTextEntry}  />
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
    backgroundColor: 'white',
    width: '70%',
    maxWidth: 400,
    marginVertical: 5,
    marginHorizontal:5
  },
  input: {
    // fontFamily: 'Montserrat-SemiBold',
  },
  error: {
    color: 'red', 
    fontSize: 12,
    backgroundColor: '#94B5E1',
    // fontFamily: 'Montserrat-SemiBold',
  }
})

export default CustomButton;