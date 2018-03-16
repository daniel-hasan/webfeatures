#!/bin/bash
python wiki-quality-web/manage.py test scheduler.tests.tests_doc_io
python wiki-quality-web/manage.py test scheduler.tests.tests_oldestfirst_io
python wiki-quality-web/manage.py test scheduler.tests.tests_small_job_first_io
python wiki-quality-web/manage.py test scheduler.tests.scheduler_run_io
python wiki-quality-web/manage.py shell < scheduler/tests/tests_run_usedfeat
