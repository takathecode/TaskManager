import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


# ==========================================================
# DADOS
# ==========================================================

tarefas = []
agendamentos = []

ARQUIVO = "tarefas.json"


# ==========================================================
# FUNÇÕES DE ARQUIVO
# ==========================================================

def carregar_dados():
    global tarefas, agendamentos

    if os.path.exists(ARQUIVO):
        try:
            with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

                tarefas = dados.get("tarefas", [])
                agendamentos = dados.get("agendamentos", [])

        except:
            tarefas = []
            agendamentos = []


def salvar_dados():
    dados = {
        "tarefas": tarefas,
        "agendamentos": agendamentos
    }

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


# ==========================================================
# FUNÇÕES DO DASHBOARD
# ==========================================================

def atualizar_dashboard():
    total = len(tarefas)

    pendentes = 0
    concluidas = 0

    for tarefa in tarefas:
        if tarefa["status"] == "Concluída":
            concluidas += 1
        else:
            pendentes += 1

    label_total.config(text=str(total))
    label_pendentes.config(text=str(pendentes))
    label_concluidas.config(text=str(concluidas))


# ==========================================================
# TELA INICIAL
# ==========================================================

def mostrar_inicio():
    limpar_conteudo()

    titulo = tk.Label(
        conteudo,
        text="DASHBOARD",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8",
        fg="#1f2937"
    )
    titulo.pack(anchor="w", pady=(10, 25))

    # Cards
    cards = tk.Frame(conteudo, bg="#f4f6f8")
    cards.pack(fill="x")

    global label_total
    global label_pendentes
    global label_concluidas

    card1 = tk.Frame(cards, bg="white", width=200, height=120)
    card1.pack(side="left", padx=10)
    card1.pack_propagate(False)

    tk.Label(
        card1,
        text="TOTAL DE TAREFAS",
        bg="white",
        fg="#555555",
        font=("Arial", 10)
    ).pack(pady=(20, 5))

    label_total = tk.Label(
        card1,
        text="0",
        bg="white",
        fg="#2563eb",
        font=("Arial", 25, "bold")
    )
    label_total.pack()

    card2 = tk.Frame(cards, bg="white", width=200, height=120)
    card2.pack(side="left", padx=10)
    card2.pack_propagate(False)

    tk.Label(
        card2,
        text="PENDENTES",
        bg="white",
        fg="#555555",
        font=("Arial", 10)
    ).pack(pady=(20, 5))

    label_pendentes = tk.Label(
        card2,
        text="0",
        bg="white",
        fg="#f59e0b",
        font=("Arial", 25, "bold")
    )
    label_pendentes.pack()

    card3 = tk.Frame(cards, bg="white", width=200, height=120)
    card3.pack(side="left", padx=10)
    card3.pack_propagate(False)

    tk.Label(
        card3,
        text="CONCLUÍDAS",
        bg="white",
        fg="#555555",
        font=("Arial", 10)
    ).pack(pady=(20, 5))

    label_concluidas = tk.Label(
        card3,
        text="0",
        bg="white",
        fg="#16a34a",
        font=("Arial", 25, "bold")
    )
    label_concluidas.pack()

    atualizar_dashboard()


# ==========================================================
# LIMPAR ÁREA PRINCIPAL
# ==========================================================

def limpar_conteudo():
    for widget in conteudo.winfo_children():
        widget.destroy()


# ==========================================================
# TELA DE TAREFAS
# ==========================================================

def mostrar_tarefas():
    limpar_conteudo()

    titulo = tk.Label(
        conteudo,
        text="TAREFAS",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    )
    titulo.pack(anchor="w", pady=10)

    # Área dos filtros
    filtros = tk.Frame(conteudo, bg="#f4f6f8")
    filtros.pack(fill="x", pady=10)

    tk.Label(
        filtros,
        text="Pesquisar:",
        bg="#f4f6f8"
    ).pack(side="left")

    global entrada_pesquisa

    entrada_pesquisa = tk.Entry(filtros, width=25)
    entrada_pesquisa.pack(side="left", padx=5)

    tk.Label(
        filtros,
        text="Prioridade:",
        bg="#f4f6f8"
    ).pack(side="left", padx=(20, 5))

    global filtro_prioridade

    filtro_prioridade = ttk.Combobox(
        filtros,
        values=["Todas", "Alta", "Média", "Baixa"],
        state="readonly",
        width=12
    )
    filtro_prioridade.set("Todas")
    filtro_prioridade.pack(side="left")

    tk.Label(
        filtros,
        text="Status:",
        bg="#f4f6f8"
    ).pack(side="left", padx=(20, 5))

    global filtro_status

    filtro_status = ttk.Combobox(
        filtros,
        values=["Todos", "Pendente", "Em andamento", "Concluída"],
        state="readonly",
        width=15
    )
    filtro_status.set("Todos")
    filtro_status.pack(side="left")

    tk.Button(
        filtros,
        text="Pesquisar",
        command=atualizar_tabela
    ).pack(side="left", padx=10)

    # Tabela
    tabela_frame = tk.Frame(conteudo)
    tabela_frame.pack(fill="both", expand=True)

    global tabela

    colunas = (
        "ID",
        "Tarefa",
        "Responsável",
        "Prioridade",
        "Data",
        "Horário",
        "Status"
    )

    tabela = ttk.Treeview(
        tabela_frame,
        columns=colunas,
        show="headings"
    )

    for coluna in colunas:
        tabela.heading(coluna, text=coluna)

    tabela.column("ID", width=40)
    tabela.column("Tarefa", width=180)
    tabela.column("Responsável", width=130)
    tabela.column("Prioridade", width=90)
    tabela.column("Data", width=100)
    tabela.column("Horário", width=80)
    tabela.column("Status", width=110)

    tabela.pack(fill="both", expand=True)

    # Botões
    botoes = tk.Frame(conteudo, bg="#f4f6f8")
    botoes.pack(fill="x", pady=10)

    tk.Button(
        botoes,
        text="+ Nova tarefa",
        command=nova_tarefa,
        bg="#2563eb",
        fg="white",
        padx=15
    ).pack(side="left", padx=5)

    tk.Button(
        botoes,
        text="✏ Editar",
        command=editar_tarefa,
        padx=15
    ).pack(side="left", padx=5)

    tk.Button(
        botoes,
        text="✓ Concluir",
        command=concluir_tarefa,
        padx=15
    ).pack(side="left", padx=5)

    tk.Button(
        botoes,
        text="🗑 Excluir",
        command=excluir_tarefa,
        padx=15
    ).pack(side="left", padx=5)

    atualizar_tabela()


# ==========================================================
# ATUALIZAR TABELA
# ==========================================================

def atualizar_tabela():
    for item in tabela.get_children():
        tabela.delete(item)

    pesquisa = entrada_pesquisa.get().lower()
    prioridade = filtro_prioridade.get()
    status = filtro_status.get()

    for tarefa in tarefas:

        if pesquisa not in tarefa["titulo"].lower():
            continue

        if prioridade != "Todas":
            if tarefa["prioridade"] != prioridade:
                continue

        if status != "Todos":
            if tarefa["status"] != status:
                continue

        tabela.insert(
            "",
            "end",
            values=(
                tarefa["id"],
                tarefa["titulo"],
                tarefa["responsavel"],
                tarefa["prioridade"],
                tarefa["data"],
                tarefa["horario"],
                tarefa["status"]
            )
        )


# ==========================================================
# NOVA TAREFA
# ==========================================================

def nova_tarefa():
    janela_tarefa = tk.Toplevel(janela)
    janela_tarefa.title("Nova tarefa")
    janela_tarefa.geometry("500x600")
    janela_tarefa.resizable(False, False)

    tk.Label(
        janela_tarefa,
        text="Nova tarefa",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    # Título
    tk.Label(janela_tarefa, text="Título:").pack(anchor="w", padx=30)

    entrada_titulo = tk.Entry(janela_tarefa, width=55)
    entrada_titulo.pack(padx=30, pady=5)

    # Descrição
    tk.Label(janela_tarefa, text="Descrição:").pack(anchor="w", padx=30)

    entrada_descricao = tk.Text(
        janela_tarefa,
        width=40,
        height=5
    )
    entrada_descricao.pack(padx=30, pady=5)

    # Responsável
    tk.Label(janela_tarefa, text="Responsável:").pack(anchor="w", padx=30)

    entrada_responsavel = tk.Entry(janela_tarefa, width=55)
    entrada_responsavel.pack(padx=30, pady=5)

    # Prioridade
    tk.Label(janela_tarefa, text="Prioridade:").pack(anchor="w", padx=30)

    entrada_prioridade = ttk.Combobox(
        janela_tarefa,
        values=["Alta", "Média", "Baixa"],
        state="readonly"
    )
    entrada_prioridade.set("Média")
    entrada_prioridade.pack(padx=30, pady=5)

    # Data
    tk.Label(janela_tarefa, text="Data:").pack(anchor="w", padx=30)

    entrada_data = tk.Entry(janela_tarefa, width=55)
    entrada_data.pack(padx=30, pady=5)

    # Horário
    tk.Label(janela_tarefa, text="Horário:").pack(anchor="w", padx=30)

    entrada_horario = tk.Entry(janela_tarefa, width=55)
    entrada_horario.pack(padx=30, pady=5)

    # Status
    tk.Label(janela_tarefa, text="Status:").pack(anchor="w", padx=30)

    entrada_status = ttk.Combobox(
        janela_tarefa,
        values=["Pendente", "Em andamento", "Concluída"],
        state="readonly"
    )
    entrada_status.set("Pendente")
    entrada_status.pack(padx=30, pady=5)

    def salvar_tarefa():

        titulo = entrada_titulo.get().strip()
        data = entrada_data.get().strip()
        horario = entrada_horario.get().strip()
        prioridade = entrada_prioridade.get()

        if titulo == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o título da tarefa."
            )
            return

        if data == "":
            messagebox.showwarning(
                "Atenção",
                "Informe a data."
            )
            return

        if horario == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o horário."
            )
            return

        if prioridade == "":
            messagebox.showwarning(
                "Atenção",
                "Informe a prioridade."
            )
            return

        novo_id = len(tarefas) + 1

        tarefa = {
            "id": novo_id,
            "titulo": titulo,
            "descricao": entrada_descricao.get("1.0", "end").strip(),
            "responsavel": entrada_responsavel.get().strip(),
            "prioridade": prioridade,
            "data": data,
            "horario": horario,
            "status": entrada_status.get()
        }

        tarefas.append(tarefa)

        salvar_dados()

        messagebox.showinfo(
            "Sucesso",
            "Tarefa cadastrada!"
        )

        janela_tarefa.destroy()

        mostrar_tarefas()

    tk.Button(
        janela_tarefa,
        text="SALVAR TAREFA",
        command=salvar_tarefa,
        bg="#2563eb",
        fg="white",
        padx=20,
        pady=8
    ).pack(pady=15)


# ==========================================================
# CONCLUIR TAREFA
# ==========================================================

def concluir_tarefa():

    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )
        return

    item = tabela.item(selecionado[0])
    id_tarefa = int(item["values"][0])

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["status"] = "Concluída"

    salvar_dados()

    atualizar_tabela()
    atualizar_dashboard()

    messagebox.showinfo(
        "Sucesso",
        "Tarefa concluída!"
    )


# ==========================================================
# EXCLUIR TAREFA
# ==========================================================

def excluir_tarefa():

    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )
        return

    item = tabela.item(selecionado[0])
    id_tarefa = int(item["values"][0])

    confirmar = messagebox.askyesno(
        "Confirmar",
        "Deseja realmente excluir esta tarefa?"
    )

    if confirmar:

        for tarefa in tarefas:
            if tarefa["id"] == id_tarefa:
                tarefas.remove(tarefa)
                break

        salvar_dados()

        atualizar_tabela()
        atualizar_dashboard()


# ==========================================================
# EDITAR TAREFA
# ==========================================================

def editar_tarefa():

    selecionado = tabela.selection()

    if not selecionado:
        messagebox.showwarning(
            "Atenção",
            "Selecione uma tarefa."
        )
        return

    item = tabela.item(selecionado[0])
    id_tarefa = int(item["values"][0])

    tarefa_encontrada = None

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa_encontrada = tarefa
            break

    if tarefa_encontrada is None:
        return

    janela_editar = tk.Toplevel(janela)
    janela_editar.title("Editar tarefa")
    janela_editar.geometry("500x550")

    tk.Label(
        janela_editar,
        text="Editar tarefa",
        font=("Arial", 20, "bold")
    ).pack(pady=15)

    tk.Label(janela_editar, text="Título:").pack(anchor="w", padx=30)

    titulo = tk.Entry(janela_editar, width=55)
    titulo.insert(0, tarefa_encontrada["titulo"])
    titulo.pack(padx=30, pady=5)

    tk.Label(janela_editar, text="Responsável:").pack(anchor="w", padx=30)

    responsavel = tk.Entry(janela_editar, width=55)
    responsavel.insert(0, tarefa_encontrada["responsavel"])
    responsavel.pack(padx=30, pady=5)

    tk.Label(janela_editar, text="Prioridade:").pack(anchor="w", padx=30)

    prioridade = ttk.Combobox(
        janela_editar,
        values=["Alta", "Média", "Baixa"],
        state="readonly"
    )
    prioridade.set(tarefa_encontrada["prioridade"])
    prioridade.pack(padx=30, pady=5)

    tk.Label(janela_editar, text="Data:").pack(anchor="w", padx=30)

    data = tk.Entry(janela_editar, width=55)
    data.insert(0, tarefa_encontrada["data"])
    data.pack(padx=30, pady=5)

    tk.Label(janela_editar, text="Horário:").pack(anchor="w", padx=30)

    horario = tk.Entry(janela_editar, width=55)
    horario.insert(0, tarefa_encontrada["horario"])
    horario.pack(padx=30, pady=5)

    tk.Label(janela_editar, text="Status:").pack(anchor="w", padx=30)

    status = ttk.Combobox(
        janela_editar,
        values=["Pendente", "Em andamento", "Concluída"],
        state="readonly"
    )
    status.set(tarefa_encontrada["status"])
    status.pack(padx=30, pady=5)

    def salvar_edicao():

        if titulo.get().strip() == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o título."
            )
            return

        tarefa_encontrada["titulo"] = titulo.get().strip()
        tarefa_encontrada["responsavel"] = responsavel.get().strip()
        tarefa_encontrada["prioridade"] = prioridade.get()
        tarefa_encontrada["data"] = data.get().strip()
        tarefa_encontrada["horario"] = horario.get().strip()
        tarefa_encontrada["status"] = status.get()

        salvar_dados()

        janela_editar.destroy()

        mostrar_tarefas()

    tk.Button(
        janela_editar,
        text="SALVAR ALTERAÇÕES",
        command=salvar_edicao,
        bg="#2563eb",
        fg="white"
    ).pack(pady=20)


# ==========================================================
# AGENDA
# ==========================================================

def mostrar_agenda():

    limpar_conteudo()

    tk.Label(
        conteudo,
        text="📅 AGENDA",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    ).pack(anchor="w", pady=10)

    formulario = tk.Frame(conteudo, bg="white", padx=20, pady=20)
    formulario.pack(fill="x", pady=10)

    tk.Label(
        formulario,
        text="Título do compromisso:",
        bg="white"
    ).grid(row=0, column=0, sticky="w")

    titulo = tk.Entry(formulario, width=50)
    titulo.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(
        formulario,
        text="Data:",
        bg="white"
    ).grid(row=1, column=0, sticky="w")

    data = tk.Entry(formulario, width=50)
    data.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(
        formulario,
        text="Horário:",
        bg="white"
    ).grid(row=2, column=0, sticky="w")

    horario = tk.Entry(formulario, width=50)
    horario.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(
        formulario,
        text="Local:",
        bg="white"
    ).grid(row=3, column=0, sticky="w")

    local = tk.Entry(formulario, width=50)
    local.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(
        formulario,
        text="Descrição:",
        bg="white"
    ).grid(row=4, column=0, sticky="nw")

    descricao = tk.Text(
        formulario,
        width=38,
        height=4
    )
    descricao.grid(row=4, column=1, padx=10, pady=5)

    def agendar():

        if titulo.get().strip() == "":
            messagebox.showwarning(
                "Atenção",
                "Informe o título."
            )
            return

        if data.get().strip() == "":
            messagebox.showwarning(
                "Atenção",
                "Informe a data."
            )
            return

        compromisso = {
            "titulo": titulo.get().strip(),
            "data": data.get().strip(),
            "horario": horario.get().strip(),
            "local": local.get().strip(),
            "descricao": descricao.get("1.0", "end").strip()
        }

        agendamentos.append(compromisso)

        salvar_dados()

        messagebox.showinfo(
            "Sucesso",
            "Compromisso agendado!"
        )

        mostrar_agenda()

    tk.Button(
        formulario,
        text="AGENDAR",
        command=agendar,
        bg="#2563eb",
        fg="white",
        padx=20
    ).grid(row=5, column=1, pady=10)

    # Lista
    tk.Label(
        conteudo,
        text="PRÓXIMOS AGENDAMENTOS",
        font=("Arial", 16, "bold"),
        bg="#f4f6f8"
    ).pack(anchor="w", pady=10)

    tabela_agenda = ttk.Treeview(
        conteudo,
        columns=("Data", "Horário", "Título", "Local"),
        show="headings"
    )

    tabela_agenda.heading("Data", text="Data")
    tabela_agenda.heading("Horário", text="Horário")
    tabela_agenda.heading("Título", text="Título")
    tabela_agenda.heading("Local", text="Local")

    tabela_agenda.pack(fill="both", expand=True)

    for compromisso in agendamentos:
        tabela_agenda.insert(
            "",
            "end",
            values=(
                compromisso["data"],
                compromisso["horario"],
                compromisso["titulo"],
                compromisso["local"]
            )
        )


# ==========================================================
# CHECKBUTTON
# ==========================================================

def mostrar_configuracoes():

    limpar_conteudo()

    tk.Label(
        conteudo,
        text="⚙ CONFIGURAÇÕES",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    ).pack(anchor="w", pady=10)

    concluida = tk.BooleanVar()

    tk.Checkbutton(
        conteudo,
        text="Mostrar tarefas concluídas",
        variable=concluida,
        bg="#f4f6f8"
    ).pack(anchor="w", pady=20)

    tk.Label(
        conteudo,
        text="Configurações básicas do TaskManager.",
        bg="#f4f6f8",
        font=("Arial", 12)
    ).pack(anchor="w")


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

carregar_dados()

janela = tk.Tk()

janela.title("TaskManager")
janela.geometry("1100x700")
janela.minsize(900, 600)

# Menu lateral
menu = tk.Frame(
    janela,
    bg="#1e293b",
    width=220
)
menu.pack(side="left", fill="y")

menu.pack_propagate(False)

tk.Label(
    menu,
    text="TASKMANAGER",
    bg="#1e293b",
    fg="white",
    font=("Arial", 18, "bold")
).pack(pady=(30, 40))

tk.Button(
    menu,
    text="🏠  Início",
    command=mostrar_inicio,
    bg="#1e293b",
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    relief="flat",
    font=("Arial", 12),
    anchor="w",
    padx=20
).pack(fill="x", pady=5)

tk.Button(
    menu,
    text="📋  Tarefas",
    command=mostrar_tarefas,
    bg="#1e293b",
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    relief="flat",
    font=("Arial", 12),
    anchor="w",
    padx=20
).pack(fill="x", pady=5)

tk.Button(
    menu,
    text="📅  Agenda",
    command=mostrar_agenda,
    bg="#1e293b",
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    relief="flat",
    font=("Arial", 12),
    anchor="w",
    padx=20
).pack(fill="x", pady=5)

tk.Button(
    menu,
    text="⚙  Configurações",
    command=mostrar_configuracoes,
    bg="#1e293b",
    fg="white",
    activebackground="#334155",
    activeforeground="white",
    relief="flat",
    font=("Arial", 12),
    anchor="w",
    padx=20
).pack(fill="x", pady=5)


# Área principal
conteudo = tk.Frame(
    janela,
    bg="#f4f6f8"
)

conteudo.pack(
    side="right",
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# Inicia no Dashboard
mostrar_inicio()

janela.mainloop()