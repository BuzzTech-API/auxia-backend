# auxia/usecases/graph.py

import io
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
import seaborn as sns



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

# 1. Distribuição das notas por métrica
def create_score_distribution_charts(docs, score_keys):
    charts = {}
    for key in score_keys:
        values = [d["scores"][key] for d in docs if key in d["scores"]]
        fig, ax = plt.subplots()
        ax.hist(values, bins=range(0, 12), alpha=0.7)
        ax.set_title(f'Distribuição das notas - {key.replace("_", " ").title()}')
        ax.set_xlabel('Nota')
        ax.set_ylabel('Frequência')
        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        charts[key] = buf
    return charts

# 2. Viés por posição
def create_position_preference_chart(docs):
    pos1 = sum(1 for d in docs if d["preferred_position"] == 1)
    pos2 = sum(1 for d in docs if d["preferred_position"] == 2)
    fig, ax = plt.subplots()
    ax.bar(["Primeira resposta", "Segunda resposta"], [pos1, pos2])
    ax.set_title("Viés de preferência por posição")
    ax.set_ylabel("Número de vezes preferida")
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

# 3. Correlação entre métricas
def create_correlation_heatmap(docs, score_keys):
    arr = np.array([[d["scores"][k] for k in score_keys] for d in docs])
    corr = np.corrcoef(arr, rowvar=False)
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, xticklabels=score_keys, yticklabels=score_keys, fmt=".2f", ax=ax)
    ax.set_title("Correlação entre métricas")
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png")
    buf.seek(0)
    plt.close(fig)
    return buf

# 4. Nuvem de palavras das justificativas
def create_wordcloud_justifications(docs, metric):
    text = " ".join(d["justifications"].get(metric, "") for d in docs)
    if not text.strip():
        text = "Sem justificativas suficientes"
    wc = WordCloud(width=500, height=300, background_color="white").generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(f"Nuvem de palavras - {metric.replace('_', ' ').title()}")
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

# 5. Radar chart dos modelos por métrica
def create_model_radar_chart(docs, score_keys):
    models = sorted({d['ans_llm_model'] for d in docs})
    scores = {m: [0] * len(score_keys) for m in models}
    counts = {m: [0] * len(score_keys) for m in models}
    for d in docs:
        model = d["ans_llm_model"]
        for i, k in enumerate(score_keys):
            scores[model][i] += d["scores"][k]
            counts[model][i] += 1
    avg_scores = {m: [scores[m][i] / counts[m][i] if counts[m][i] else 0 for i in range(len(score_keys))] for m in models}

    angles = np.linspace(0, 2 * np.pi, len(score_keys), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    for model in models:
        vals = avg_scores[model] + avg_scores[model][:1]
        ax.plot(angles, vals, label=model)
        ax.fill(angles, vals, alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([k.replace('_', ' ').title() for k in score_keys])
    ax.set_title("Desempenho médio dos modelos por métrica")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

