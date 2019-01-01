from django.urls import path
from . import views

app_name = "vote"
urlpatterns = [
    path("", view=views.Vote_main.as_view(), name='main_view'),
    path("add/candi", view=views.Add_candi.as_view(), name='add_candi'),
    path("add/poll", view=views.Add_poll.as_view(), name='add_poll'),
    path("canditopoll", view=views.Candi_to_poll.as_view(), name='candi_to_poll'),
    path("getpolls/<int:id>", view=views.getPoll, name='get_poll'), #ajax
    path("<str:area>/<int:id>", view=views.Vote_area.as_view(), name='area'),
    path("select/<int:id>/<int:poll_id>", view=views.Vote_select.as_view(), name='select'),
]
