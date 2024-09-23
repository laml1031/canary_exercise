from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import User
import requests
from urllib.parse import parse_qs

GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
GITHUB_CLIENT_ID = settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET
VUE_BASED_URL = settings.VUE_BASED_URL
GOOGLE_OAUTH_REDIRECT_URI = VUE_BASED_URL + "/google-login-success"
GITHUB_OAUTH_REDIRECT_URI = VUE_BASED_URL + "/github-login-success"


class GoogleOAuthView(APIView):
    def get(self, request):
        # Redirect to Google OAuth page
        return HttpResponseRedirect(
            "https://accounts.google.com/o/oauth2/v2/auth?"
            + "client_id="
            + GOOGLE_CLIENT_ID
            + "&redirect_uri="
            + GOOGLE_OAUTH_REDIRECT_URI
            + "&response_type=code&scope=openid+profile+email"
        )


class GoogleOAuthCallbackView(APIView):
    def get(self, request):
        # Handle Google OAuth callback
        code = request.GET.get("code")
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": GOOGLE_OAUTH_REDIRECT_URI,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
        }
        response = requests.post(token_url, data=data)
        token = response.json()["access_token"]
        user_url = "https://openidconnect.googleapis.com/v1/userinfo"
        headers = {"Authorization": "Bearer " + token}
        user_response = requests.get(user_url, headers=headers)
        user = {}
        user["name"] = user_response.json()["name"]
        user["email"] = user_response.json()["email"]
        #Check if user already exists in DB, if not create a new user
        try:
            saveUser = User.objects.get(google_id=user["email"])
        except User.DoesNotExist:
            saveUser = User(google_id=user["email"])
            saveUser.save() 
        #   user = User.objects.create(google_id=response.json()['id'])
        return Response({"user": user})


class GitHubOAuthView(APIView):
    def get(self, request):
        # Redirect to GitHub OAuth page
        return HttpResponseRedirect(
            "https://github.com/login/oauth/authorize?"
            + "client_id="
            + GITHUB_CLIENT_ID
            + "&redirect_uri="
            + GITHUB_OAUTH_REDIRECT_URI
            + "&scope=repo"
        )


class GitHubOAuthCallbackView(APIView):
    def get(self, request):
        # Handle GitHub OAuth callback
        code = request.GET.get("code")
        google_user_id = request.GET.get("google_user_id")
        
        token_url = "https://github.com/login/oauth/access_token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": GITHUB_OAUTH_REDIRECT_URI,
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
        }
        response = requests.post(token_url, headers=headers, data=data)
        response_json = parse_qs(response.text)
        token = response_json["access_token"][0]

        # Get user's GitHub username
        user_url = "https://api.github.com/user"
        headers = {"Authorization": "Bearer " + token}
        user_response = requests.get(user_url, headers=headers)
        githubUser = {}
        githubUser["username"] = user_response.json()["login"]

        # Get user's GitHub repositories
        repo_url = "https://api.github.com/user/repos"
        repo_response = requests.get(repo_url, headers=headers)
        repos = repo_response.json()

        # Save GitHub token in DB
        user = User.objects.get(google_id=google_user_id)
        user.github_id = githubUser["username"]
        user.github_token = token
        selected_repo = user.selected_repo
        user.save()



        return Response({"githubUser": githubUser, "repos": repos, "selected_repo": selected_repo})


class GitHubRepoSelectView(APIView):
    def post(self, request):
        # Store selected repository in DB
        user = User.objects.get(google_id=request.data["google_user_id"])
        user.selected_repo = request.data["repo"]
        user.save()
        return Response({"message": "Repository selected"})


