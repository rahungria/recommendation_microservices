JIKAN_API_Path = 'https://api.jikan.moe/v3'

# test profiles
# dongers
# Raphailias
# mattusi
# marcelloscat


ANIME_MASK = [             # full anime request
    #"request_hash",         #
    "request_cached",        # if true skip sleep, if false sleep (4) sec # seems broken  
    #"request_cache_expiry", #
    "mal_id",                #
    "url",                   #
    #"image_url",            #
    #"trailer_url",          #
    "title",                 #
    #"title_english",        #
    #"title_japanese",       #
    #"title_synonyms",       #
    "type",                  #
    "source",                #
    "episodes",              #
    #"status",               #
    #"airing",               #
    #"aired",                #
    #"duration",             #
    #"rating",               #
    "score",                 #
    "scored_by",             #
    "rank",                  #
    "popularity",            #
    "members",               #
    "favorites",             #
    #"synopsis",             #
    #"background",           #
    "premiered",             #
    "broadcast",             #
    #"related",              #
    #"producers",            #
    #"licensors",            #
    "studios",               # []
    "genres",                # []
    #"opening_themes",       #
    #"ending_themes"         #
]

SEASON_ANIME_MASK= [
    "mal_id",                #
    "url",                   #
    "title",                 #
    "image_url",             #
    "synopsis",              #
    "type",                  #
    "airing_start",          #
    "episodes",              #
    "members",               # sort by for popularity ?
    "genres",                # []
    "source",                #
    "producers",             # []
    "score",                 # sort by score
    #"licensors",            #
    #"r18",                  #
    #"kids",                 #
    #"continuing",           #
]

USER_ANIME_MASK= [
    "mal_id",                #
    "title",                 #
    #"video_url",            #
    "url",                   #
    "image_url",             #
    "type",                  #
    "watching_status",       #
    "score",                 # 0 = unrated
    #"watched_episodes",     #
    #"total_episodes",       #
    #"airing_status",        #
    #"season_name",          #
    #"season_year",          #
    #"has_episode_video",    #
    #"has_promo_video",      #
    #"has_video",            #
    #"is_rewatching",        #
    "tags",                  #
    #"rating",               #
    "start_date",            #
    #"end_date",             #
    #"watch_start_date",     #
    #"watch_end_date",       #
    #"days",                 #
    #"storage",              #
    #"priority",             #
    #"added_to_list",        #
    "studios",               # []
    #"licensors",            # []
]


def parse_xreadgroup(unparsed):
    return {
        streams[0]: [{'id': msg[0], 'msg': msg[1]} for msg in streams[1]]
        for streams in unparsed
    }


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {iteration}/{total} => {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
