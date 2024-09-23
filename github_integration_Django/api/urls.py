from django.urls import path
from . import views
from . import webhooks

urlpatterns = [
    path("google-oauth/", views.GoogleOAuthView.as_view(), name="google-oauth"),
    path(
        "google-oauth-callback/",
        views.GoogleOAuthCallbackView.as_view(),
        name="google-oauth-callback",
    ),
    path("github-oauth/", views.GitHubOAuthView.as_view(), name="github-oauth"),
    path(
        "github-oauth-callback/",
        views.GitHubOAuthCallbackView.as_view(),
        name="github-oauth-callback",
    ),
    path(
        "github-repo-select/",
        views.GitHubRepoSelectView.as_view(),
        name="github-repo-select",
    ),
    path("webhook/", webhooks.github_webhook, name="webhook"),
]
