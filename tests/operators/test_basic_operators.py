"""
Tests for basic operators in rxpy_opkit.
"""

import unittest
from loguru import logger

import reactivex as rx
from reactivex import operators as ops
from reactivex.testing import TestScheduler, ReactiveTest

# Will import custom operators here later
# from rxpy_opkit.operators import custom_operator


class TestBasicOperators(unittest.TestCase):
    """Test cases for basic RxPy operators."""
    
    def setUp(self):
        """Set up test environment."""
        self.scheduler_TestScheduler = TestScheduler()
        
    def test_standard_rxpy_operator(self):
        """Test that standard RxPy operators work as expected."""
        on_next = ReactiveTest.on_next
        
        # Create test observable with test scheduler
        source = self.scheduler_TestScheduler.create_hot_observable(
            on_next(150, 1),
            on_next(210, 2),
            on_next(220, 3),
        )
        
        # Apply standard operators
        result = source.pipe(
            ops.map(lambda x: x * 10)
        )
        
        # Create observer
        observer = self.scheduler_TestScheduler.create_observer()
        result.subscribe(observer)
        
        # Run the virtual time
        self.scheduler_TestScheduler.start()
        
        # Check results
        expected = [
            on_next(210, 20),
            on_next(220, 30),
        ]
        
        # Assert results match expectations
        self.assertEqual(expected, observer.messages)
