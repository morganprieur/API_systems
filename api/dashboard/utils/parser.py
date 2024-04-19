from datetime import timedelta, datetime 
import re 
d = re.compile('[\d]+') 


def filter_last(mLast): 

    # Le nombre dans le param last : 
    mLastNum = re.search(d, mLast).group() 
    now = datetime.now() 

    # Valeurs possibles pour from : 
    # h (hours), d (days), m (minutes) 
    # le temps à retirer de l'heure présente 
    if mLast.endswith('h'): 
        delta = timedelta(hours=int(mLastNum)) 
    elif mLast.endswith('d'): 
        delta = timedelta(days=int(mLastNum)) 
    elif mLast.endswith('m'): 
        delta = timedelta(minutes=int(mLastNum)) 

    targetLast = now - delta  

    return targetLast 

