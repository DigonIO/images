import datetime as dt

import pytest
from helpers import _TZ_ERROR_MSG, START_STOP_ERROR, TZ_ERROR_MSG, utc

from scheduler import SchedulerError
from scheduler.job import Job, JobType
from scheduler.trigger import Trigger


@pytest.mark.skip("Currently under redesign")
@pytest.mark.parametrize(
    "job_type, timing, start, stop, tzinfo, err",
    (
        [JobType.WEEKLY, [Trigger.Weekly.Monday()], None, None, None, None],
        [
            JobType.WEEKLY,
            [Trigger.Weekly.Monday(), Trigger.Weekly.Thursday()],
            None,
            None,
            None,
            None,
        ],
        [JobType.WEEKLY, [Trigger.Weekly.Monday()], None, None, utc, None],
        [
            JobType.DAILY,
            [dt.time(tzinfo=utc)],
            dt.datetime.now(utc),
            None,
            utc,
            None,
        ],
        [
            JobType.DAILY,
            [dt.time(tzinfo=utc)],
            dt.datetime.now(utc),
            None,
            utc,
            None,
        ],
        [
            JobType.DAILY,
            [dt.time(tzinfo=None)],
            dt.datetime.now(utc),
            None,
            utc,
            TZ_ERROR_MSG,
        ],
        [
            JobType.DAILY,
            [dt.time(tzinfo=None)],
            None,
            None,
            utc,
            TZ_ERROR_MSG,
        ],
        [
            JobType.DAILY,
            [dt.time(tzinfo=None)],
            None,
            dt.datetime.now(utc),
            utc,
            TZ_ERROR_MSG,
        ],
        [
            JobType.DAILY,
            [dt.time()],
            dt.datetime.now(utc),
            None,
            None,
            _TZ_ERROR_MSG.format("start"),
        ],
        [
            JobType.DAILY,
            [dt.time()],
            None,
            dt.datetime.now(utc),
            None,
            _TZ_ERROR_MSG.format("stop"),
        ],
        [
            JobType.WEEKLY,
            [Trigger.Weekly.Monday()],
            dt.datetime.now(utc),
            dt.datetime.now(utc) - dt.timedelta(hours=1),
            utc,
            START_STOP_ERROR,
        ],
    ),
)
def test_job_init(
    job_type,
    timing,
    start,
    stop,
    tzinfo,
    err,
):
    if err:
        with pytest.raises(SchedulerError, match=err):
            Job(
                job_type=job_type,
                timing=timing,
                handle=lambda: None,
                kwargs={},
                max_attempts=1,
                weight=20,
                start=start,
                stop=stop,
                tzinfo=tzinfo,
            )
    else:
        Job(
            job_type=job_type,
            timing=timing,
            handle=lambda: None,
            kwargs={},
            max_attempts=1,
            weight=20,
            start=start,
            stop=stop,
            tzinfo=tzinfo,
        )
