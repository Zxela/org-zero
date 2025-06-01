# tests/core/models/test_job_tracking.py
import unittest
from core.models.job_tracking import create_job, update_job_status, get_job, list_jobs, JobStatus

class TestJobTracking(unittest.TestCase):
    def test_create_and_get_job(self):
        job = create_job(job_type="test_task", payload="payload1")
        self.assertIsNotNone(job.id)
        fetched = get_job(job.id)
        self.assertEqual(fetched.id, job.id)
        self.assertEqual(fetched.type, "test_task")
        self.assertEqual(fetched.status, JobStatus.PENDING)

    def test_update_job_status(self):
        job = create_job(job_type="test_update", payload="payload2")
        update_job_status(job.id, JobStatus.RUNNING)
        updated = get_job(job.id)
        self.assertEqual(updated.status, JobStatus.RUNNING)
        update_job_status(job.id, JobStatus.SUCCESS, result="done")
        updated2 = get_job(job.id)
        self.assertEqual(updated2.status, JobStatus.SUCCESS)
        self.assertEqual(updated2.result, "done")

    def test_list_jobs(self):
        job1 = create_job(job_type="list1", payload="a")
        job2 = create_job(job_type="list2", payload="b")
        jobs = list_jobs()
        self.assertTrue(any(j.id == job1.id for j in jobs))
        self.assertTrue(any(j.id == job2.id for j in jobs))
        # Filter by status
        update_job_status(job1.id, JobStatus.FAILED)
        failed_jobs = list_jobs(status=JobStatus.FAILED)
        self.assertTrue(any(j.id == job1.id for j in failed_jobs))
        self.assertFalse(any(j.id == job2.id for j in failed_jobs))

if __name__ == "__main__":
    unittest.main()
