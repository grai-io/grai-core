from grai_source_fivetran.loader import FivetranGraiMapper


def test_fivetran_grai_mapper():
    from dotenv import load_dotenv

    load_dotenv()
    mapper = FivetranGraiMapper()
    breakpoint()
