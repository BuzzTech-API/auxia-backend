import io
import re
import base64
import json
from itertools import combinations
from collections import defaultdict

from typing import Annotated
from fastapi import APIRouter, Request, Security, status
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import markdown

from auxia.models.answer import AnswerModel
from auxia.schemas.answer import AnswerExport, AnswerRequest
from auxia.schemas.usuario import UserOut
from auxia.usecases.answer import answer_usecase
from auxia.usecases.auth import get_current_active_user
from auxia.usecases.graph import (
    create_stacked_bar,
    create_pie_chart,
    create_comparison_chart,
    create_score_distribution_charts,
    create_position_preference_chart,
    create_correlation_heatmap,
    create_wordcloud_justifications,
    create_model_radar_chart,
)

router = APIRouter(prefix="/answer", tags=["answer"])
templates = Jinja2Templates(directory="static")

@router.post("", status_code=status.HTTP_201_CREATED)
async def saveAnswer(
    current_user: Annotated[
        UserOut, Security(get_current_active_user, scopes=["awnsers"])
    ],
    awnserOne: AnswerRequest,
    awnserTwo: AnswerRequest,
):
    awnserOneModel = AnswerModel(**awnserOne.model_dump(), ans_pair_position=1)
    awnserTwoModel = AnswerModel(**awnserTwo.model_dump(), ans_pair_position=2)
    awnserTwoModel.ans_pair_id = awnserOneModel.ans_pair_id
    awnserOneSaved = await answer_usecase.saveAnswer(awnserOneModel) 
    awnserTwoSaved = await answer_usecase.saveAnswer(awnserTwoModel) 
    return 


@router.get(
    "/export",
    summary="Exporta todas as respostas em NDJSON para treinamento de LLMs",
    response_class=StreamingResponse,
)
async def export_answers(
    current_user: Annotated[UserOut, Security(get_current_active_user, scopes=["export"])],
):
    cursor = answer_usecase.collection.find({})

    async def generator():
        async for doc in cursor:
            # 1) Monta scores e justificativas
            score_keys = [
                "aderencia_prompt",
                "coerencia_clareza",
                "exatidao_confiabilidade",
                "exposicao_justificativa",
                "idioma_pergunta_mesmo_resposta",
                "resposta_agressiva_ofensiva",
            ]
            scores = {key: doc.get(f"ans_{key}_pontuation", 0) for key in score_keys}
            justs  = {key: doc.get(f"ans_{key}_justify", "")    for key in score_keys}

            # 2) Extrai preferred_position de ans_prefered_answer
            pref_text = doc.get("ans_prefered_answer", "") or ""
            # primeiro tenta LLM1/LLM2
            m = re.search(r"LLM\s*([12])", pref_text, re.IGNORECASE)
            # se não achar, tenta dígito isolado
            if not m:
                m = re.search(r"\b([12])\b", pref_text)
            preferred_position = int(m.group(1)) if m else None

            # 3) Monta o objeto de exportação
            export_obj = {
                "ans_pair_id":         doc.get("ans_pair_id", ""),
                "ans_pair_position":   doc.get("ans_pair_position", 0),
                "preferred_position":  preferred_position,
                "prompt":              doc.get("ans_prompt", ""),
                "completion":          doc.get("ans_llm_answer", ""),
                "model":               doc.get("ans_llm_model", ""),
                "scores":              scores,
                "justifications":      justs,
                "preferred_text":      pref_text,
                "preferred_justify":   doc.get("ans_prefered_answer_justify", ""),
                "is_rag":              doc.get("ans_is_rag", False),
            }

            # 4) Gera uma linha NDJSON
            yield json.dumps(export_obj, ensure_ascii=False) + "\n"

    return StreamingResponse(
        generator(),
        media_type="application/x-ndjson",
        headers={"Content-Disposition": "attachment; filename=answers_export.ndjson"},
    )

@router.get(
    "/export/pdf",
    summary="Exporta relatório em PDF",
    status_code=status.HTTP_200_OK,
)
async def export_pdf(current_user=Security(get_current_active_user, scopes=["export"])):
    raw_docs = [doc async for doc in answer_usecase.collection.find({})]

    # Enriquecer docs
    score_keys = [
        "aderencia_prompt",
        "coerencia_clareza",
        "exatidao_confiabilidade",
        "exposicao_justificativa",
        "idioma_pergunta_mesmo_resposta",
        "resposta_agressiva_ofensiva",
    ]
    docs = []
    for d in raw_docs:
        scores = {k: d.get(f"ans_{k}_pontuation", 0) for k in score_keys}
        justs  = {k: d.get(f"ans_{k}_justify", "")   for k in score_keys}

        # extrai posição preferida: primeiro LLM1/LLM2, depois dígito isolado
        pref_text = d.get("ans_prefered_answer", "") or ""
        m = re.search(r"LLM\s*([12])", pref_text, re.IGNORECASE)
        if not m:
            m = re.search(r"\b([12])\b", pref_text)
        preferred_position = int(m.group(1)) if m else None

        answer_html = markdown.markdown(d.get("ans_llm_answer", ""))

        docs.append({
            **d,
            "scores": scores,
            "justifications": justs,
            "preferred_position": preferred_position,
            "answer_html": answer_html,
        })

    total_answers = len(docs)

    # gera gráficos...
    bar_chart = base64.b64encode(create_stacked_bar(docs).read()).decode()
    models    = sorted({d["ans_llm_model"] for d in docs})
    pie_charts = {
        m: base64.b64encode(create_pie_chart(docs, m).read()).decode()
        for m in models
    }

    comparison_charts = {}
    if len(models) > 1:
        for x, y in combinations(models, 2):
            buf = create_comparison_chart(docs, x, y)
            comparison_charts[f"{x}_vs_{y}"] = base64.b64encode(buf.read()).decode()

    score_dist_charts = create_score_distribution_charts(docs, score_keys)
    score_dist_charts_b64 = {k: base64.b64encode(v.read()).decode() for k, v in score_dist_charts.items()}

    position_pref_chart_b64 = base64.b64encode(create_position_preference_chart(docs).read()).decode()
    correlation_chart_b64 = base64.b64encode(create_correlation_heatmap(docs, score_keys).read()).decode()
    radar_chart_b64 = base64.b64encode(create_model_radar_chart(docs, score_keys).read()).decode()

    wordclouds_b64 = {}
    for k in score_keys:
        buf = create_wordcloud_justifications(docs, k)
        wordclouds_b64[k] = base64.b64encode(buf.read()).decode()
    totals = {m: [] for m in models}
    for d in docs:
        totals[d["ans_llm_model"]].append(sum(d["scores"].values()))
    avg_scores = {m: (sum(v)/len(v) if v else 0) for m, v in totals.items()}
    best_model = max(avg_scores, key=avg_scores.get) if avg_scores else None

    rag_totals    = [sum(d["scores"].values()) for d in docs if d.get("ans_is_rag")]
    no_rag_totals = [sum(d["scores"].values()) for d in docs if not d.get("ans_is_rag")]
    avg_rag    = sum(rag_totals)/len(rag_totals) if rag_totals else 0
    avg_no_rag = sum(no_rag_totals)/len(no_rag_totals) if no_rag_totals else 0
    rag_made_difference = avg_rag > avg_no_rag

    pairs = defaultdict(list)
    for d in docs:
        key = (d["ans_prompt"], d.get("ans_pair_id", ""))
        pairs[key].append(d)

    env = Environment(loader=FileSystemLoader("static"), autoescape=True)
    template = env.get_template("report.html")
    with open("static/logo.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

    html = template.render(
        logo_base64=logo_b64,
        total_answers=total_answers,
        bar_chart=bar_chart,
        pie_charts=pie_charts,
        comparison_charts=comparison_charts,
        models=models,
        avg_scores=avg_scores,
        avg_rag=avg_rag,
        avg_no_rag=avg_no_rag,
        best_model=best_model,
        rag_made_difference=rag_made_difference,
        pairs=pairs,
        score_dist_charts=score_dist_charts_b64,
        position_pref_chart=position_pref_chart_b64,
        correlation_chart=correlation_chart_b64,
        radar_chart=radar_chart_b64,
        wordclouds=wordclouds_b64,
        score_keys=score_keys,
    )

    pdf = HTML(string=html).write_pdf()
    return StreamingResponse(
        io.BytesIO(pdf),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=relatorio_avaliacoes.pdf"},
    )

@router.get(
    "/export/html",
    summary="Preview do HTML que vira PDF",
    response_class=HTMLResponse,
 )
async def preview_html(request: Request):
    raw_docs = [doc async for doc in answer_usecase.collection.find({})]
    score_keys = [
        "aderencia_prompt","coerencia_clareza","exatidao_confiabilidade",
        "exposicao_justificativa","idioma_pergunta_mesmo_resposta",
        "resposta_agressiva_ofensiva"
    ]
    docs = []
    for d in raw_docs:
        scores = {k: d.get(f"ans_{k}_pontuation", 0) for k in score_keys}
        justs  = {k: d.get(f"ans_{k}_justify", "")    for k in score_keys}

        # extrai posição preferida: primeiro LLM1/LLM2, depois dígito isolado
        pref_text = d.get("ans_prefered_answer", "") or ""
        m = re.search(r"LLM\s*([12])", pref_text, re.IGNORECASE)
        if not m:
            m = re.search(r"\b([12])\b", pref_text)
        preferred_position = int(m.group(1)) if m else None

        answer_html = markdown.markdown(d.get("ans_llm_answer", ""))

        docs.append({
            **d,
            "scores": scores,
            "justifications": justs,
            "preferred_position": preferred_position,
            "answer_html": answer_html,
        })

    total_answers = len(docs)

    bar  = base64.b64encode(create_stacked_bar(docs).read()).decode()
    models = sorted({d["ans_llm_model"] for d in docs})
    pies   = {m: base64.b64encode(create_pie_chart(docs,m).read()).decode() for m in models}
    comparison_charts = {}
    if len(models) > 1:
        for x, y in combinations(models, 2):
            key = f"{x}_vs_{y}"
            buf = create_comparison_chart(docs, x, y)
            comparison_charts[key] = base64.b64encode(buf.read()).decode()

    score_dist_charts = create_score_distribution_charts(docs, score_keys)
    score_dist_charts_b64 = {k: base64.b64encode(v.read()).decode() for k, v in score_dist_charts.items()}

    position_pref_chart_b64 = base64.b64encode(create_position_preference_chart(docs).read()).decode()
    correlation_chart_b64 = base64.b64encode(create_correlation_heatmap(docs, score_keys).read()).decode()
    radar_chart_b64 = base64.b64encode(create_model_radar_chart(docs, score_keys).read()).decode()

    wordclouds_b64 = {}
    for k in score_keys:
        buf = create_wordcloud_justifications(docs, k)
        wordclouds_b64[k] = base64.b64encode(buf.read()).decode()

    totals = {m: [] for m in models}
    for d in docs:
        totals[d["ans_llm_model"]].append(sum(d["scores"].values()))
    avg_scores = {m:(sum(v)/len(v) if v else 0) for m,v in totals.items()}
    best_model = max(avg_scores, key=avg_scores.get) if avg_scores else None

    rag_totals    = [sum(d["scores"].values()) for d in docs if d.get("ans_is_rag")]
    no_rag_totals = [sum(d["scores"].values()) for d in docs if not d.get("ans_is_rag")]
    avg_rag    = sum(rag_totals)/len(rag_totals) if rag_totals else 0
    avg_no_rag = sum(no_rag_totals)/len(no_rag_totals) if no_rag_totals else 0
    rag_made_difference = avg_rag > avg_no_rag

    pairs = defaultdict(list)
    for d in docs:
        pairs[(d["ans_prompt"], d.get("ans_pair_id",""))].append(d)

    with open("static/logo.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

    return templates.TemplateResponse("report.html", {
        "request": request,
        "logo_base64": logo_b64,
        "total_answers": total_answers,
        "bar_chart": bar,
        "pie_charts": pies,
        "comparison_charts": comparison_charts,
        "models": models,
        "avg_scores": avg_scores,
        "avg_rag": avg_rag,
        "avg_no_rag": avg_no_rag,
        "best_model": best_model,
        "rag_made_difference": rag_made_difference,
        "pairs": pairs,
        "score_dist_charts":score_dist_charts_b64,
        "position_pref_chart":position_pref_chart_b64,
        "correlation_chart":correlation_chart_b64,
        "radar_chart":radar_chart_b64,
        "wordclouds":wordclouds_b64,
        "score_keys":score_keys,

    })
