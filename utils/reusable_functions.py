from userprofiles.models import SeenMovie, SavedMovie

def is_movie_seen(movie_id, current_user):
    try:
        SeenMovie.objects.get(movie_id=movie_id, seen_by=current_user)
        seen_list = True
    except:
        seen_list = False
    return seen_list

def is_movie_saved(movie_id, current_user):
    try:
        SavedMovie.objects.get(movie_id=movie_id, saved_by=current_user)
        seen_list = True
    except:
        seen_list = False
    return seen_list


# If functions not reused, put somewhere else ?