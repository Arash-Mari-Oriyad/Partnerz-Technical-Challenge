import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from qa_agent import answer_question

@pytest.mark.parametrize("query", [
    "How do I reset my password?",
    "What integrations does Intercom support?",
    "Can I change my billing cycle mid-subscription?"
])
def test_answer_nonempty(query):
    answer = answer_question(query)
    assert isinstance(answer, str)
    assert len(answer.strip()) > 0
