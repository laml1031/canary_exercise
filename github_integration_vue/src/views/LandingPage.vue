<template>  
    <div>  
     <h1>Landing Page</h1>  
     <button @click="googleLogin">Login with Google</button>  
    </div>  
  </template>  
    
  <script>  
  export default {  
    methods: {  
     googleLogin() {  
      window.location.href = 'http://localhost:8000/api/google-oauth/'  
     }  
    }  
  }  
  </script>