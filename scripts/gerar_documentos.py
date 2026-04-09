#!/usr/bin/env python3
"""Gerador de Procuração Ad Judicia e Contrato de Prestação de Serviços Advocatícios.

Uso CLI:  python3 gerar_documentos.py '<json_dados>' /caminho/saida/
Módulo:   from scripts.gerar_documentos import gerar_procuracao, gerar_contrato
"""

import json
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

# ============================================================
# DADOS FIXOS DO ESCRITÓRIO
# ============================================================

ADV1_NOME = "BRUNO MELO DE CARVALHO"
ADV1_OAB_LONG = "OAB/GO sob nº 58.029"
ADV1_EMAIL = "brunomelo.jus@gmail.com"

ADV2_NOME = "RAFAEL MELO DE CARVALHO"
ADV2_OAB_LONG = "OAB/GO sob o nº 59.244"
ADV2_EMAIL = "rafaelmelojus@gmail.com"

ENDERECO_ESCRITORIO = (
    "Avenida Deputado Jamel Cecílio, nº 2496, Sala 72-B, "
    "Edifício New Business Style, Jardim Goiás, Goiânia - GO CEP 74.810-100"
)

BANCO = (
    "Banco Nubank (260), Agência 0001, Conta 8334231-7, "
    "em nome de Bruno Melo de Carvalho (CPF: 051.128.971-55)"
)

# ============================================================
# ESTILOS
# ============================================================

_BASE_SIZE = 11
_LEADING = _BASE_SIZE * 1.5

S = {
    "normal": ParagraphStyle(
        "normal", fontName="Helvetica", fontSize=_BASE_SIZE,
        leading=_LEADING, alignment=TA_JUSTIFY,
    ),
    "titulo": ParagraphStyle(
        "titulo", fontName="Helvetica-Bold", fontSize=_BASE_SIZE,
        leading=_LEADING, alignment=TA_CENTER,
    ),
    "clausula": ParagraphStyle(
        "clausula", fontName="Helvetica-Bold", fontSize=_BASE_SIZE,
        leading=_LEADING, alignment=TA_JUSTIFY,
    ),
    "corpo": ParagraphStyle(
        "corpo", fontName="Helvetica", fontSize=_BASE_SIZE,
        leading=_LEADING, alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm,
    ),
    "centro": ParagraphStyle(
        "centro", fontName="Helvetica", fontSize=_BASE_SIZE,
        leading=_LEADING, alignment=TA_CENTER,
    ),
    "assinatura": ParagraphStyle(
        "assinatura", fontName="Helvetica", fontSize=_BASE_SIZE,
        leading=_LEADING, alignment=TA_CENTER,
    ),
    "assinatura_bold": ParagraphStyle(
        "assinatura_bold", fontName="Helvetica-Bold", fontSize=_BASE_SIZE,
        leading=_LEADING, alignment=TA_CENTER,
    ),
}

# ============================================================
# HELPERS
# ============================================================


def b(text):
    """Negrito inline para uso dentro de Paragraph()."""
    return f"<b>{text}</b>"


def sp(n=1):
    """Espaço vertical. sp() = simples, sp(2) = duplo, etc."""
    return Spacer(1, 0.3 * cm * n)


def _make_doc(path):
    return SimpleDocTemplate(
        str(path), pagesize=A4,
        leftMargin=3 * cm, rightMargin=2 * cm,
        topMargin=2.5 * cm, bottomMargin=2 * cm,
    )


def _file_name(tipo, nome):
    """Gera nome: Tipo_PRIMEIRO_ULTIMO.pdf"""
    parts = nome.strip().split()
    if len(parts) >= 2:
        return f"{tipo}_{parts[0]}_{parts[-1]}.pdf"
    return f"{tipo}_{parts[0]}.pdf"


# ============================================================
# PROCURAÇÃO AD JUDICIA
# ============================================================


def gerar_procuracao(d, output_path):
    """Gera PDF da Procuração Ad Judicia."""
    doc = _make_doc(output_path)
    story = []

    # Título
    story.append(Paragraph('PROCURAÇÃO "AD JUDICIA"', S["titulo"]))
    story.append(sp(2))

    # Outorgante
    story.append(Paragraph(
        f'<b>OUTORGANTE:</b> {b(d["nome"])}, {d["nacionalidade"]}, '
        f'{d["estado_civil"]}, {d["profissao"]}, inscrito(a) no CPF sob o '
        f'nº {b(d["cpf"])}, residente e domiciliado(a) em {d["endereco"]}.',
        S["normal"]
    ))
    story.append(sp())

    # Outorgados
    story.append(Paragraph(
        f'<b>OUTORGADOS:</b> {b(ADV1_NOME)}, advogado, inscrito na '
        f'{ADV1_OAB_LONG}, e {b(ADV2_NOME)}, advogado, inscrito na '
        f'{ADV2_OAB_LONG}, com escritório profissional situado na '
        f'{ENDERECO_ESCRITORIO}, endereços eletrônicos: {ADV1_EMAIL} e '
        f'{ADV2_EMAIL}.',
        S["normal"]
    ))
    story.append(sp(2))

    # Poderes gerais
    story.append(Paragraph(
        'Pelo presente instrumento particular de procuração, o(a) OUTORGANTE '
        'acima qualificado(a) nomeia e constitui como seus bastantes '
        'procuradores os OUTORGADOS acima identificados, a quem confere amplos '
        'poderes para o foro em geral, com as cláusulas "ad judicia et extra", '
        'podendo propor contra quem de direito as ações competentes e defender '
        'os direitos do(a) outorgante nas contrárias, seguindo umas e outras '
        'até final decisão, usando todos os recursos legais e acompanhando-os, '
        'conferindo-lhes ainda poderes especiais para confessar, desistir, '
        'transigir, firmar compromissos ou acordos, receber e dar quitação, '
        'agindo em conjunto ou separadamente, podendo, ainda, substabelecer '
        'esta a outrem, com ou sem reservas de iguais poderes, dando tudo por '
        'bom, firme e valioso.',
        S["normal"]
    ))
    story.append(sp())

    # Poderes específicos
    story.append(Paragraph(
        f'A presente procuração é outorgada especificamente para fins de '
        f'{b(d["acao"])}, conforme previsto no art. 103 e seguintes do Novo '
        f'Código de Processo Civil (Lei nº 13.105/2015).',
        S["normal"]
    ))
    story.append(sp(3))

    # Local e data
    story.append(Paragraph(f'{d["cidade"]}, {d["data"]}.', S["centro"]))
    story.append(sp(4))

    # Assinatura
    story.append(Paragraph("________________________________", S["assinatura"]))
    story.append(Paragraph(d["nome"], S["assinatura_bold"]))
    story.append(Paragraph("(Outorgante)", S["assinatura"]))

    doc.build(story)


# ============================================================
# CONTRATO DE PRESTAÇÃO DE SERVIÇOS ADVOCATÍCIOS
# ============================================================


def gerar_contrato(d, output_path):
    """Gera PDF do Contrato de Prestação de Serviços Advocatícios (9 cláusulas)."""
    doc = _make_doc(output_path)
    story = []

    # Título
    story.append(Paragraph(
        "CONTRATO DE PRESTAÇÃO DE SERVIÇOS ADVOCATÍCIOS", S["titulo"]
    ))
    story.append(sp(2))

    # ---- Preâmbulo ----
    story.append(Paragraph(
        f'Pelo presente instrumento particular de contrato de prestação de '
        f'serviços advocatícios, de um lado, como <b>CONSTITUINTE</b>, '
        f'{b(d["nome"])}, {d["nacionalidade"]}, {d["estado_civil"]}, '
        f'{d["profissao"]}, inscrito(a) no CPF sob o nº {b(d["cpf"])}, '
        f'residente e domiciliado(a) em {d["endereco"]};',
        S["normal"]
    ))
    story.append(sp())

    story.append(Paragraph(
        f'E, de outro lado, como <b>CONSTITUÍDOS</b>, {b(ADV1_NOME)}, '
        f'advogado, inscrito na {ADV1_OAB_LONG}, e {b(ADV2_NOME)}, advogado, '
        f'inscrito na {ADV2_OAB_LONG}, com escritório profissional situado na '
        f'{ENDERECO_ESCRITORIO};',
        S["normal"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'Têm entre si, justo e contratado, o presente Contrato de Prestação '
        'de Serviços Advocatícios, que se regerá pelas cláusulas e condições '
        'seguintes:',
        S["normal"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA PRIMEIRA ----
    story.append(Paragraph(
        "CLÁUSULA PRIMEIRA – DO OBJETO / OBRIGAÇÕES DO CONSTITUÍDO",
        S["clausula"]
    ))
    story.append(sp())

    story.append(Paragraph(
        f'O(A) CONSTITUINTE contrata os serviços advocatícios dos CONSTITUÍDOS '
        f'para representá-lo(a) na {b(d["acao"])}, perante o {d["vara"]}, '
        f'compreendendo as seguintes atividades:',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'I – Elaboração e protocolo da petição inicial, bem como o '
        'acompanhamento de todos os atos processuais até a decisão final '
        'em primeira instância;',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'II – Acompanhamento e manifestação em todas as intimações, '
        'audiências, perícias e demais atos processuais necessários ao '
        'andamento regular do feito.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        '§ 1º – Os serviços contratados não incluem recursos a instâncias '
        'superiores (Tribunais de Justiça, Tribunais Superiores ou Supremo '
        'Tribunal Federal), que dependerão de novo ajuste contratual.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        '§ 2º – Eventuais serviços advocatícios não previstos neste contrato '
        'serão objeto de contrato suplementar.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA SEGUNDA ----
    story.append(Paragraph(
        "CLÁUSULA SEGUNDA – DOS HONORÁRIOS / OBRIGAÇÕES DO CONSTITUINTE",
        S["clausula"]
    ))
    story.append(sp())

    story.append(Paragraph(
        f'I – Pelos serviços prestados, o(a) CONSTITUINTE pagará aos '
        f'CONSTITUÍDOS o valor de {b(d["honorarios_valor"])}.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        f'§ 1º – {d["honorarios_pagamento"]}.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        '§ 2º – O atraso no pagamento dos honorários acarretará multa '
        'de 30% (trinta por cento) sobre o valor devido, acrescido de '
        'juros moratórios de 1% (um por cento) ao mês, sem prejuízo '
        'da correção monetária.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        '§ 3º – Os valores dos honorários serão corrigidos anualmente '
        'pelo índice IGP-M/FGV, ou por outro índice que venha a '
        'substituí-lo.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        f'§ 4º – Os pagamentos deverão ser realizados mediante '
        f'transferência bancária para: {BANCO}.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'III – As custas processuais, emolumentos, taxas judiciárias e '
        'demais despesas necessárias ao andamento do processo são de '
        'responsabilidade exclusiva do(a) CONSTITUINTE, não estando '
        'incluídas nos honorários advocatícios.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'IV – O(A) CONSTITUINTE se obriga a fornecer todos os documentos '
        'e informações necessários à propositura e ao acompanhamento da '
        'demanda judicial.',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'VI – Em caso de inadimplência do(a) CONSTITUINTE, as partes '
        'celebram negócio jurídico processual, nos termos do art. 190 do '
        'Código de Processo Civil, autorizando a penhora de até 30% '
        '(trinta por cento) dos rendimentos líquidos do(a) CONSTITUINTE '
        'para satisfação do débito.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA TERCEIRA ----
    story.append(Paragraph("CLÁUSULA TERCEIRA – DA SUCUMBÊNCIA", S["clausula"]))
    story.append(sp())

    story.append(Paragraph(
        'Os honorários de sucumbência fixados judicialmente pertencem '
        'integralmente aos advogados CONSTITUÍDOS, conforme disposto no '
        'art. 23 da Lei nº 8.906/94 (Estatuto da Advocacia e da OAB), '
        'não se compensando com os honorários contratuais previstos na '
        'Cláusula Segunda.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA QUARTA ----
    story.append(Paragraph("CLÁUSULA QUARTA – DA VIGÊNCIA", S["clausula"]))
    story.append(sp())

    story.append(Paragraph(
        'O presente contrato vigorará a partir da data de sua assinatura '
        'até a prática do último ato processual na demanda objeto deste '
        'instrumento, incluindo a fase de cumprimento de sentença, se houver.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA QUINTA ----
    story.append(Paragraph("CLÁUSULA QUINTA – DA REPRESENTAÇÃO", S["clausula"]))
    story.append(sp())

    story.append(Paragraph(
        'O presente contrato não é personalíssimo, podendo os CONSTITUÍDOS '
        'serem representados por advogado associado ou substabelecido para '
        'a prática de atos processuais específicos, sem prejuízo de sua '
        'responsabilidade perante o(a) CONSTITUINTE.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA SEXTA ----
    story.append(Paragraph(
        "CLÁUSULA SEXTA – DAS OBRIGAÇÕES DO CONSTITUINTE", S["clausula"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'Constituem obrigações do(a) CONSTITUINTE:', S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'I – Fornecer todos os documentos, informações e elementos '
        'necessários à instrução do processo;',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'II – Arcar com as custas processuais e despesas necessárias '
        'ao andamento da demanda;',
        S["corpo"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'III – Comunicar imediatamente aos CONSTITUÍDOS qualquer '
        'mudança de endereço, telefone ou demais dados de contato.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA SÉTIMA ----
    story.append(Paragraph(
        "CLÁUSULA SÉTIMA – DAS OBRIGAÇÕES DOS SUCESSORES", S["clausula"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'As obrigações assumidas neste contrato se estendem aos herdeiros '
        'e sucessores das partes, a qualquer título.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA OITAVA ----
    story.append(Paragraph(
        "CLÁUSULA OITAVA – DAS DISPOSIÇÕES LEGAIS", S["clausula"]
    ))
    story.append(sp())

    story.append(Paragraph(
        'O presente contrato é regido pela Lei nº 8.906/94 (Estatuto da '
        'Advocacia e da Ordem dos Advogados do Brasil), pelo Código de '
        'Ética e Disciplina da OAB, pelo Código Civil Brasileiro e demais '
        'legislações aplicáveis.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- CLÁUSULA NONA ----
    story.append(Paragraph("CLÁUSULA NONA – DO FORO", S["clausula"]))
    story.append(sp())

    story.append(Paragraph(
        f'As partes elegem o foro da comarca de {b(d["cidade"])} para '
        f'dirimir quaisquer dúvidas ou litígios oriundos do presente '
        f'contrato, com renúncia expressa a qualquer outro, por mais '
        f'privilegiado que seja.',
        S["corpo"]
    ))
    story.append(sp(2))

    # ---- Fecho ----
    story.append(Paragraph(
        'E por estarem assim justos e contratados, firmam o presente '
        'instrumento em 02 (duas) vias de igual teor e forma, na presença '
        'de 02 (duas) testemunhas, para que produza seus jurídicos e '
        'legais efeitos.',
        S["normal"]
    ))
    story.append(sp(2))

    # Local e data
    story.append(Paragraph(f'{d["cidade"]}, em {d["data"]}.', S["centro"]))
    story.append(sp(3))

    # Assinaturas - Advogados
    story.append(Paragraph("________________________________", S["assinatura"]))
    story.append(Paragraph(ADV1_NOME, S["assinatura_bold"]))
    story.append(Paragraph(ADV1_OAB_LONG, S["assinatura"]))
    story.append(sp(2))

    story.append(Paragraph("________________________________", S["assinatura"]))
    story.append(Paragraph(ADV2_NOME, S["assinatura_bold"]))
    story.append(Paragraph(ADV2_OAB_LONG, S["assinatura"]))
    story.append(sp(2))

    # Assinatura - Cliente
    story.append(Paragraph("________________________________", S["assinatura"]))
    story.append(Paragraph(d["nome"], S["assinatura_bold"]))
    story.append(Paragraph(f'CPF: {d["cpf"]}', S["assinatura"]))
    story.append(Paragraph("(Constituinte)", S["assinatura"]))
    story.append(sp(3))

    # Testemunhas
    story.append(Paragraph("<b>TESTEMUNHAS:</b>", S["normal"]))
    story.append(sp(2))

    story.append(Paragraph("01. ________________________________", S["normal"]))
    story.append(Paragraph("Nome:", S["normal"]))
    story.append(Paragraph("CPF:", S["normal"]))
    story.append(sp(2))

    story.append(Paragraph("02. ________________________________", S["normal"]))
    story.append(Paragraph("Nome:", S["normal"]))
    story.append(Paragraph("CPF:", S["normal"]))

    doc.build(story)


# ============================================================
# MAIN (CLI)
# ============================================================


def main():
    if len(sys.argv) < 3:
        print(f"Uso: python3 {sys.argv[0]} '<json_dados>' /caminho/saida/")
        sys.exit(1)

    dados = json.loads(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    nome = dados["nome"]
    print(f"Gerando documentos para: {nome}")

    proc_path = output_dir / _file_name("Procuracao", nome)
    cont_path = output_dir / _file_name("Contrato", nome)

    gerar_procuracao(dados, proc_path)
    print(f"  ✓ Salvo: {proc_path}")

    gerar_contrato(dados, cont_path)
    print(f"  ✓ Salvo: {cont_path}")

    print(f"\nConcluído! Arquivos gerados em {output_dir}")


if __name__ == "__main__":
    main()
