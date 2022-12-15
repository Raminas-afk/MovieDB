from userprofiles.models import SeenMovie, SavedMovie

def is_movie_seen(movie_id, current_profile):
    try:
        SeenMovie.objects.get(movie_id=movie_id, profiles=current_profile)
        seen_list = True
    except:
        seen_list = False
    return seen_list

def is_movie_saved(movie_id, current_profile):
    try:
        SavedMovie.objects.get(movie_id=movie_id, profiles=current_profile)
        seen_list = True
    except:
        seen_list = False
    return seen_list


# If functions not reused, put somewhere else ?