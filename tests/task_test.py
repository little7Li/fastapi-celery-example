# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""Test celery tasks."""

from unittest import TestCase

from main import long_task


class TestTasks(TestCase):
    """Unit test for tasks."""

    def test_long_task(self):
        """Test for long task."""
        task = long_task.s().apply()
        self.assertEqual(task.status, "SUCCESS")
        self.assertEqual(
            task.info, {
                "current": 100,
                "total": 100,
                "status": "Task completed!",
                "result": 42,
            })
