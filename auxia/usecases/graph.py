# auxia/usecases/graph.py

import io
from collections import defaultdict
import matplotlib.pyplot as plt

def create_pie_chart(docs, model):
    """
    Pie chart de preferência COM vs SEM RAG para `model`.
    Se não houver preferências registradas, gera fatias 0×0
    para evitar NaN e desenha legendas corretamente.
    """
    # conta preferências válidas
    pref_rag = 0
    pref_no  = 0
    for d in docs:
        if d["ans_llm_model"] != model:
            continue
        if d.get("preferred_position") == d.get("ans_pair_position"):
            if d.get("ans_is_rag", False):
                pref_rag += 1
            else:
                pref_no += 1


        total = pref_rag + pref_no
    sizes = [pref_rag or 1, pref_no or 1]
    labels = ["Preferido com RAG", "Preferido sem RAG"]

    fig, ax = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=lambda pct: f"{int(round(pct * total / 100))}" if total else "0",
        startangle=90
    )
    ax.set_title(f"Preferência RAG vs Sem RAG – {model}", pad=20)
    ax.axis("equal")

    # legenda no canto inferior direito, fora do círculo
    ax.legend(
        wedges,
        labels,
        title="Legenda",
        loc="lower left",
        bbox_to_anchor=(1.02, 0.02),
        borderaxespad=0
    )
    fig.subplots_adjust(right=0.75, bottom=0.1)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

def create_comparison_chart(docs, model_x, model_y):
    """
    Gráfico de barras agrupadas X vs Y:
    - Conta quantas vezes cada um foi preferido COM e SEM RAG.
    - Sempre retorna um buffer, mesmo sem pares válidos.
    """
    # agrupa por prompt+par
    pairs = defaultdict(list)
    for d in docs:
        key = (d["ans_prompt"], d.get("ans_pair_id", ""))
        pairs[key].append(d)

    # contadores
    x_pref_rag = x_pref_no = y_pref_rag = y_pref_no = 0

    for _, group in pairs.items():
        if len(group) != 2:
            continue
        # pega o dicionário de cada modelo (ou None)
        resp_x = next((d for d in group if d["ans_llm_model"] == model_x), None)
        resp_y = next((d for d in group if d["ans_llm_model"] == model_y), None)
        if not resp_x or not resp_y:
            continue

        # conta vencedor
        if resp_x.get("preferred_position") == resp_x.get("ans_pair_position"):
            if resp_x.get("ans_is_rag", False): x_pref_rag += 1
            else:                              x_pref_no  += 1
        elif resp_y.get("preferred_position") == resp_y.get("ans_pair_position"):
            if resp_y.get("ans_is_rag", False): y_pref_rag += 1
            else:                              y_pref_no  += 1

    # prepara barras (sempre com valores, mesmo que zeros)
    labels        = [model_x, model_y]
    rag_counts    = [x_pref_rag,   y_pref_rag]
    no_rag_counts = [x_pref_no,    y_pref_no]
    x_pos = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    bar1 = ax.bar([i - width/2 for i in x_pos], rag_counts,     width, label="Preferido com RAG")
    bar2 = ax.bar([i + width/2 for i in x_pos], no_rag_counts,  width, label="Preferido sem RAG")

    ax.set_xticks(list(x_pos))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.bar_label(bar1)
    ax.bar_label(bar2)
    ax.legend()

    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plt.close(fig)
    return buf

def create_stacked_bar(docs):
    models = sorted({doc['ans_llm_model'] for doc in docs})
    rag_counts = [sum(1 for d in docs if d['ans_llm_model']==m and d.get('ans_is_rag')) for m in models]
    no_rag_counts = [sum(1 for d in docs if d['ans_llm_model']==m and not d.get('ans_is_rag')) for m in models]
    x = range(len(models))
    fig, ax = plt.subplots()
    ax.bar(x, rag_counts, label="Com RAG")
    ax.bar(x, no_rag_counts, bottom=rag_counts, label="Sem RAG")
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.bar_label(ax.containers[0])  # rótulos de Com RAG :contentReference[oaicite:9]{index=9}
    ax.bar_label(ax.containers[1])  # rótulos de Sem RAG :contentReference[oaicite:10]{index=10}
    ax.legend()
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf
