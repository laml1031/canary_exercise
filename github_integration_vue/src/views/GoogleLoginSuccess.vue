<template>  
    <div>  
     <h1>Google Login Success</h1>  
     <p>Name: {{ googleUserName }}</p>  
     <p>Email: {{ googleUserEmail }}</p>  
     <button @click="githubLogin">Connect to GitHub</button>  
    </div>  
  </template>  
    
  <script>  
  import axios from 'axios';  

  export default {  
    data() {  
     return {  
      googleUserName: '',
      googleUserEmail: '', 
     }  
    },  
    mounted() {  
     const code = this.$route.query.code 
     axios.get('http://localhost:8000/api/google-oauth-callback/?code='+code)  
      .then(response => {  
        this.googleUserName = response.data['user']['name']
        this.googleUserEmail = response.data['user']['email']
        localStorage.setItem('google_user_id', this.googleUserEmail)
      })  
      .catch(error => {  
        console.error(error)  
      })  
    },  
    methods: {  
     githubLogin() {  
      window.location.href = 'http://localhost:8000/api/github-oauth/'  
     }  
    }  
  }  
  </script>
