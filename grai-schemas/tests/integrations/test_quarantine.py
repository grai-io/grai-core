from functools import cache

import pytest
from grai_schemas.integrations.base import QuarantineAccessor
from grai_schemas.integrations.quarantine import Quarantine, QuarantinedNode


def test_quarantine_has_quarantined(mock_v1):
    quarantine = Quarantine()
    assert not quarantine.has_quarantined

    quarantine.nodes = [QuarantinedNode(node=mock_v1.node.sourced_node(), reasons=[])]
    assert quarantine.has_quarantined


# Test for QuarantineAccessor class
def test_quarantine_accessor(mock_v1):
    class MockIntegration:
        def __init__(self):
            self.quarantine = QuarantineAccessor(self)

        @cache
        def nodes(self):
            self.quarantine.nodes = [mock_v1.node.sourced_node()]  # these are the wrong type but it's just for testing
            return [mock_v1.node.sourced_node() for i in range(2)]

        @cache
        def edges(self):
            self.quarantine.edges = [mock_v1.edge.sourced_edge()]  # these are the wrong type but it's just for testing
            return [mock_v1.edge.sourced_edge() for i in range(2)]

        @cache
        def events(self):
            self.quarantine.events = [mock_v1.event.event()]  # these are the wrong type but it's just for testing
            return [mock_v1.event.event() for i in range(2)]

    mock_integration = MockIntegration()

    assert len(mock_integration.nodes()) == 2
    assert len(mock_integration.quarantine.nodes) == 1

    assert len(mock_integration.edges()) == 2
    assert len(mock_integration.quarantine.edges) == 1

    assert len(mock_integration.events()) == 2
    assert len(mock_integration.quarantine.events) == 1

    # Test setters
    new_nodes = [QuarantinedNode(node=mock_v1.node.sourced_node(), reasons=[])]
    mock_integration.quarantine.nodes = new_nodes
    assert mock_integration.quarantine.nodes == new_nodes
