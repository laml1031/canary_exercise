<template>  
    <div>  
     <h1>GitHub Login Success</h1>  
     <!--p>Name: {{ googleUserName }}</p>  
     <p>Email: {{ googleUserEmail }}</p-->  
     <p>GitHub Username: {{ githubUser.username }}</p>  
     <ul>  
      <li v-for="repo in repos" :key="repo.id">  
        <input type="radio" :value="repo.id" v-model="selectedRepo">  
        {{ repo.name }}  
      </li>  
     </ul>  
    </div>  
  </template>  
    
  <script>  
  import axios from 'axios';  
  export default {  
    data() {  
     return {  
      // googleUserName: '',
      // googleUserEmail: '', 
      githubUser: {},  
      repos: [],  
      selectedRepo: ''  
     }  
    },  
    mounted() {  
      console.log(localStorage.getItem('google_user_id'))
      const code = this.$route.query.code 
      const google_user_id = localStorage.getItem('google_user_id')
      axios.get('http://localhost:8000/api/github-oauth-callback/?code='+code+'&google_user_id='+google_user_id)  
      .then(response => {  
//        this.user = response.data  
        console.log(response.data)
        this.githubUser = response.data.githubUser  
        this.repos = response.data.repos
        this.selectedRepo = response.data.selected_repo  
      })  
      .catch(error => {  
        console.error(error)  
      })  
    },  
    watch: {  
     selectedRepo(newVal) {  
      axios.post('http://localhost:8000/api/github-repo-select/', { repo: newVal, google_user_id: localStorage.getItem('google_user_id') })  
        .then(response => {  
         console.log(response.data)  
        })  
        .catch(error => {  
         console.error(error)  
        })  
     }  
    }  
  }  
  </script>