from datetime import date

from django.shortcuts import render
from ocflib.lab.stats import current_semester_start
from ocflib.lab.stats import get_connection

from ocfweb.caching import periodic

MIRRORS_EPOCH = date(2017, 1, 1)


def stats_mirrors(request):

    sem = bandwidth_semester()
    total = bandwidth_all_time()

    return render(
        request,
        'stats/mirrors.html',
        {
            'title': 'Mirrors Statistics',
            'bandwidth_semester': sem,
            'bandwidth_semester_sum': sum(b[1] for b in sem),
            'bandwidth_all_time': total,
            'bandwidth_all_time_sum': sum(b[1] for b in total),
            'start_date': current_semester_start,
        },
    )


def _bandwidth_by_dist(start):
    with get_connection() as c:
        c.execute(
            'SELECT `dist`, SUM(`up` + `down`) as `bandwidth` FROM `mirrors_public`'
            'WHERE `date` >= %s GROUP BY `dist` ORDER BY `bandwidth` DESC', start,
        )

    return [(i['dist'], float(i['bandwidth'])) for i in c]


@periodic(86400)
def bandwidth_semester():
    return _bandwidth_by_dist(current_semester_start())


@periodic(86400)
def bandwidth_all_time():
    return _bandwidth_by_dist(MIRRORS_EPOCH)
