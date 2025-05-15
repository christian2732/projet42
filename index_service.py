# Objectif : Fournir des données d’indices simulées (mock)

from index import Index

def get_mock_indices():
    return [
        Index(name="CAC 40", value=7456.12),
        Index(name="NASDAQ", value=13789.44),
        Index(name="DOW JONES", value=33990.56)
    ]
