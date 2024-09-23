import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'  
import GoogleLoginSuccess from '../views/GoogleLoginSuccess.vue'  
import GitHubLoginSuccess from '../views/GitHubLoginSuccess.vue'  

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [  
    {  
     path: '/',  
     name: 'landing-page',  
     component: LandingPage  
    },  
    {  
     path: '/google-login-success',  
     name: 'google-login-success',  
     component: GoogleLoginSuccess  
    },  
    {  
     path: '/github-login-success',  
     name: 'github-login-success',  
     component: GitHubLoginSuccess  
    }  
   ]  
})

export default router
