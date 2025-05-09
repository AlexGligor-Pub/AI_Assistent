import tkinter as tk
from tkinter import scrolledtext, Toplevel
from tkhtmlview import HTMLLabel
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Setări model Ollama
llm = Ollama(model="ayahtml")
embed_model = OllamaEmbedding(model_name="ayahtml")
Settings.llm = llm
Settings.embed_model = embed_model

# Încarcă documentele
documents = SimpleDirectoryReader(r"C:\OllamaTest\Model Training\TriningDocuments").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Afișează într-o fereastră HTML
def afiseaza_html(raspuns):
    html_win = Toplevel(root)
    html_win.title("Rezultat HTML")
    label = HTMLLabel(html_win, html=f"{raspuns}", width=80)
    label.pack(padx=10, pady=10)

# Procesare întrebare
def trimite_intrebare():
    intrebare = entry.get()
    if intrebare.strip():
        raspuns = query_engine.query(intrebare)
        output.insert(tk.END, f"Întrebare: {intrebare}\nRăspuns: {raspuns}\n\n")
        entry.delete(0, tk.END)
        afiseaza_html(str(raspuns))

# UI principal
root = tk.Tk()
root.title("Asistent AI - Întrebări despre firmă")

entry = tk.Entry(root, width=80)
entry.pack(padx=10, pady=10)

btn = tk.Button(root, text="Trimite întrebare", command=trimite_intrebare)
btn.pack(padx=10)

output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=20)
output.pack(padx=10, pady=10)

root.mainloop()
