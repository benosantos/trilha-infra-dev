
import json

from dev03_censo_equipamentos.src.censo import processar_censo


def criar_csv(caminho):
    conteudo = """carimbo,nome,telefone,vaga,notebook,serie_notebook,celular,serie_celular,chip,linha_chip
2026-11-12 08:30:00,Joao Silva,11912345678,Analista de TI,Sim,PF3A 9X7K,Sim,ABC123,Sim,11987654321
2026-11-12 08:45:00,Maria Souza,21987654321,Suporte,Sim,DELL 123,Não,,Sim,21998765432
2026-11-12 09:00:00,Carlos Lima,31932345678,Infraestrutura,Não,,Sim,Nao sei,Não,
2026-11-12 09:15:00,TESTE Automático,11912345678,Teste,Sim,TESTE123,Sim,TESTE456,Sim,11987654321
"""

    caminho.write_text(conteudo, encoding="utf-8")


def test_processar_censo_completo(tmp_path, monkeypatch):
    csv = tmp_path / "respostas.csv"
    itens = tmp_path / "itens.json"
    patrimonio = tmp_path / "patrimonio.json"

    criar_csv(csv)

    monkeypatch.setattr(
        "dev03_censo_equipamentos.src.integrador_patrimonio.ARQUIVO_PATRIMONIO",
        patrimonio,
    )

    resultado = processar_censo(csv, itens)

    assert resultado["funcionarios_lidos"] == 3
    assert resultado["itens_novos"] == 6
    assert resultado["total_itens"] == 6
    assert resultado["pendencias"] == 1

    assert itens.exists()

    dados = json.loads(itens.read_text(encoding="utf-8"))

    assert len(dados) == 6


def test_reprocessamento_nao_duplica_itens(tmp_path, monkeypatch):
    csv = tmp_path / "respostas.csv"
    itens = tmp_path / "itens.json"
    patrimonio = tmp_path / "patrimonio.json"

    criar_csv(csv)

    monkeypatch.setattr(
        "dev03_censo_equipamentos.src.integrador_patrimonio.ARQUIVO_PATRIMONIO",
        patrimonio,
    )

    primeira = processar_censo(csv, itens)
    segunda = processar_censo(csv, itens)

    assert primeira["itens_novos"] == 6
    assert segunda["itens_novos"] == 0
    assert segunda["total_itens"] == 6


def test_patrimonios_preservados_no_reprocessamento(tmp_path, monkeypatch):
    csv = tmp_path / "respostas.csv"
    itens = tmp_path / "itens.json"
    patrimonio = tmp_path / "patrimonio.json"

    criar_csv(csv)

    monkeypatch.setattr(
        "dev03_censo_equipamentos.src.integrador_patrimonio.ARQUIVO_PATRIMONIO",
        patrimonio,
    )

    primeira = processar_censo(csv, itens)
    segunda = processar_censo(csv, itens)

    codigos_primeira = [
        item["patrimonio"]
        for item in primeira["itens"]
    ]

    codigos_segunda = [
        item["patrimonio"]
        for item in segunda["itens"]
    ]

    assert codigos_primeira == codigos_segunda
