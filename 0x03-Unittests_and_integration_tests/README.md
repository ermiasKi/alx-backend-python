# Unit Testing & Integration Testing Guide

## Overview

This project demonstrates the principles of unit testing and integration testing in Python using the `unittest` framework. The tests verify the functionality of various utility functions and a GitHub API client.

## Test Structure

### Unit Tests
**Location**: `test_utils.py`  
**Purpose**: Test individual components in isolation

#### Test Classes:
1. **TestAccessNestedMap** - Tests the `access_nested_map` function
2. **TestGetJson** - Tests the `get_json` function  
3. **TestMemoize** - Tests the `memoize` decorator
4. **TestGithubOrgClient** - Tests individual methods of the GitHub client

### Integration Tests  
**Location**: `test_utils.py` (TestIntegrationGithubOrgClient class)  
**Purpose**: Test how components work together

## Key Testing Concepts

### Unit Testing
**Definition**: Testing individual units of code in isolation  
**Characteristics**:
- Tests one function/method at a time
- Uses mocks to isolate dependencies
- Fast execution
- Focuses on specific functionality

**Example**: Testing `access_nested_map` with various input combinations

### Integration Testing
**Definition**: Testing how multiple units work together  
**Characteristics**:
- Tests component interactions
- Uses minimal mocks (only external dependencies)
- Verifies data flow between components
- More realistic than unit tests

**Example**: Testing `GithubOrgClient.public_repos` which calls multiple methods

## Testing Tools Used

### unittest Framework
Python's built-in testing framework providing:
- Test case classes
- Assertion methods
- Test discovery
- Setup/teardown methods

### parameterized
Decorator for running the same test with different inputs:
```python
@parameterized.expand([
    (input1, expected1),
    (input2, expected2),
])