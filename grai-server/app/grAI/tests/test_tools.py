from grAI.tools import NHopQueryAPI
import asyncio
from workspaces.models import Workspace, Organisation
import pytest
from lineage.models import Node
from django_multitenant.utils import set_current_tenant


# @pytest.mark.django_db(transaction=True)
# def test_n_hop_query():
#
#     set_current_tenant(Organisation.objects.get(name="default"))
#     workspace = Workspace.objects.get(name="default")
#     api = NHopQueryAPI(workspace.id)
#     call_args = api.schema_model(name="grai_bigquery_demo.customers", namespace="default", request_context="")
#     result = asyncio.run(api.call(**call_args.dict()))
#
