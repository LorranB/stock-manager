import tkinter as tk

from tkinter import (
    filedialog,
    messagebox,
    ttk
)

from tkinter.scrolledtext import ScrolledText

import threading

import os

from main_precificacao import executar


pdf_selecionado = ""


def selecionar_pdf():

    global pdf_selecionado

    arquivo = filedialog.askopenfilename(

        title="Selecionar PDF",

        filetypes=[
            ("PDF", "*.pdf")
        ]
    )

    if arquivo:

        pdf_selecionado = arquivo

        label_pdf.config(

            text=os.path.basename(
                arquivo
            )
        )


def escrever_log(texto):

    logs.insert(
        tk.END,
        texto + "\n"
    )

    logs.see(tk.END)

    janela.update_idletasks()


def atualizar_progresso(
    atual,
    total
):

    barra["maximum"] = total

    barra["value"] = atual

    percentual = int(
        atual / total * 100
    )

    progresso_label.config(

        text=f"{atual}/{total} ({percentual}%)"

    )

    janela.update_idletasks()


def executar_bot():

    global pdf_selecionado

    if not pdf_selecionado:

        messagebox.showwarning(

            "Aviso",

            "Selecione um PDF."

        )

        return

    botao.config(
        state="disabled"
    )

    barra["value"] = 0

    logs.delete(
        "1.0",
        tk.END
    )

    status_var.set(
        "🟡 Processando..."
    )

    try:

        executar(

            pdf_selecionado,

            callback_log=escrever_log,

            callback_progresso=atualizar_progresso

        )

        status_var.set(
            "🟢 Finalizado"
        )

        messagebox.showinfo(

            "Concluído",

            "Arquivos gerados com sucesso!"

        )

    except Exception as erro:

        status_var.set(
            "🔴 Erro"
        )

        escrever_log(
            f"Erro: {erro}"
        )

        messagebox.showerror(

            "Erro",

            str(erro)

        )

    finally:

        botao.config(
            state="normal"
        )


def iniciar_thread():

    threading.Thread(

        target=executar_bot,

        daemon=True

    ).start()


def abrir_arquivo(nome):

    caminho = os.path.join(

        "output",

        nome

    )

    if os.path.exists(caminho):

        os.startfile(caminho)

    else:

        messagebox.showwarning(

            "Aviso",

            "Arquivo não encontrado."

        )


janela = tk.Tk()

janela.title(
    "Estoque Manager"
)

janela.geometry(
    "700x650"
)

janela.configure(
    bg="#F5FFF7"
)


titulo = tk.Label(

    janela,

    text="Estoque Manager",

    font=(
        "Arial",
        18,
        "bold"
    ),

    bg="#F5FFF7",

    fg="#2E7D32"

)

titulo.pack(
    pady=15
)


label_pdf = tk.Label(

    janela,

    text="Nenhum PDF selecionado",

    bg="#F5FFF7",

    font=("Arial", 10)

)

label_pdf.pack()


tk.Button(

    janela,

    text="Selecionar PDF",

    command=selecionar_pdf,

    bg="#81C784",

    fg="white",

    font=(
        "Arial",
        10,
        "bold"
    ),

    width=25

).pack(
    pady=10
)


botao = tk.Button(

    janela,

    text="▶ Executar Análise",

    command=iniciar_thread,

    bg="#4CAF50",

    fg="white",

    font=(
        "Arial",
        11,
        "bold"
    ),

    width=25

)

botao.pack(
    pady=10
)


style = ttk.Style()

style.theme_use(
    "default"
)

style.configure(

    "green.Horizontal.TProgressbar",

    troughcolor="#E8F5E9",

    background="#4CAF50"

)


barra = ttk.Progressbar(

    janela,

    style="green.Horizontal.TProgressbar",

    orient="horizontal",

    length=500,

    mode="determinate"

)

barra.pack(
    pady=10
)


progresso_label = tk.Label(

    janela,

    text="0/0",

    bg="#F5FFF7"

)

progresso_label.pack()


status_var = tk.StringVar()

status_var.set(
    "⚪ Pronto"
)

tk.Label(

    janela,

    textvariable=status_var,

    bg="#F5FFF7",

    font=(
        "Arial",
        10,
        "bold"
    )

).pack(
    pady=5
)


logs = ScrolledText(

    janela,

    height=15,

    width=80

)

logs.pack(

    padx=20,

    pady=15,

    fill="both",

    expand=True

)


frame_botoes = tk.Frame(

    janela,

    bg="#F5FFF7"

)

frame_botoes.pack(
    pady=10
)


tk.Button(

    frame_botoes,

    text="Relatório",

    command=lambda: abrir_arquivo(
        "relatorio_precificacao.txt"
    ),

    bg="#81C784",

    fg="white"

).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(

    frame_botoes,

    text="Lista WhatsApp",

    command=lambda: abrir_arquivo(
        "lista_whatsapp.txt"
    ),

    bg="#81C784",

    fg="white"

).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(

    frame_botoes,

    text="Histórico de Preços",

    command=lambda: abrir_arquivo(
        "historico_precos.csv"
    ),

    bg="#81C784",

    fg="white"

).grid(
    row=0,
    column=2,
    padx=5
)


janela.mainloop()
