import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
import tkinter.messagebox as msg

import customtkinter as ctk
from rdflib import Graph


class App:
    GRAPH_IRI: str = "./resources/ecology.rdf"
    PREFIXES: tuple[str] = (
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
        "PREFIX owl: <http://www.w3.org/2002/07/owl#>",
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>",
        "PREFIX ont: <http://www.semanticweb.org/egorp/ontologies/2024/11/untitled-ontology-20#>"   # Возможно надо менять 
    )
    QUERIES = {
        "SELECT" : """
        SELECT ?название_материала ?автор ?тема
            WHERE {
                ?материал ont:Название_материала ?название_материала .
                ?материал ont:Материал_Активиста ?активист .
                ?активист ont:ФИО_активиста ?автор .
                ?материал ont:Материал_о_Проблеме ?проблема .
                ?проблема ont:Направленность_деятельности ?тема
            }
        """,
        "CONSTRUCT" : """
        CONSTRUCT {
            ?материал ont:Название_материала ?название .
            ?материал ont:Материал_Aктивиста ?автор .
        }
            WHERE {
                ?материал ont:Название_материала ?название .
                ?материал ont:Материал_Aктивиста ?автор .
            }
        """,
        "ASK" : """
        ASK {
            ?активист ont:ФИО_активиста "Кубанин Андрей Анатольевич" .
        }
        """
    }
    
    def __init__(self):
        ctk.set_appearance_mode('light')
        ctk.set_widget_scaling(1.4)
        
        self.root = ctk.CTk()
        self.root.title("Охрана Природы")
        self.root.geometry("+500+300")
        
        self.graph = Graph()
        self.graph.parse(self.GRAPH_IRI)
        
        self.set_query_txt()
        self.set_predefined()
    
    def set_query_txt(self) -> None:
        frame = ctk.CTkFrame(self.root)
        frame.pack(side="top", expand=True, fill='both')
        
        self.query_txt = st.ScrolledText(
            frame, 
            height=10
        )
        self.query_txt.grid(row=0, column=1, rowspan=4, padx=10, pady=10)
        
        ctk.CTkButton(
            frame, 
            text="Выполнить запрос",
            command=lambda: self.execute_query(self.query_txt.get("1.0", tk.END).strip())
        ).grid(row=1, column=0, padx=10, pady=10)
        
        self.table_check_var = tk.IntVar(value=1)
        ctk.CTkCheckBox(
            frame, text="В виде таблицы", variable=self.table_check_var
        ).grid(row=2, column=0, padx=10, pady=10)
        
        self.prefixes_check_var = tk.IntVar(value=0)
        ctk.CTkCheckBox(
            frame, text="Без префиксов", variable=self.prefixes_check_var
        ).grid(row=3, column=0, padx=10, pady=10)
        
    def set_predefined(self) -> None:
        frame = ctk.CTkFrame(self.root)
        frame.pack(side="bottom", expand=True, fill='both')
        
        buttons = 0
        for title, query in self.QUERIES.items():
            ctk.CTkButton(
                frame, 
                text=title,
                command=lambda q=query: self.query_txt.insert('1.0', q.strip())
            ).grid(row=0, column=buttons, padx=5, pady=5)
            buttons += 1
        
        ctk.CTkButton(
            frame, 
            text="Очистить",
            command=self.clear_query
        ).grid(row=0, column=buttons, padx=5, pady=5)
        
    def clear_query(self) -> None:
        self.query_txt.delete("1.0", tk.END)
        
    def execute_query(self, query: str) -> None:
        if not query:
            msg.showwarning("Ошибка", "Поле запроса пустое")
            return
        try:
            results = self.graph.query(
                self.add_prefixes(query) if self.prefixes_check_var.get() == 0 else query
            )
            
            if not results.vars:
                if self.table_check_var.get() == 1:
                    self.create_results_table(['ASK'], [[results.askAnswer]])
                else:
                    self.create_results_text([[results.askAnswer]])
                return
            
            parsed_data = [] 
            for row in results:
                parsed_data.append([row.get(var) for var in results.vars])
            
            if self.table_check_var.get() == 1:
                self.create_results_table(
                    column_names=results.vars,
                    data=parsed_data
                )
            else:
                self.create_results_text(parsed_data)
            
        except Exception as e:
            msg.showerror("Ошибка", str(e))
    
    def add_prefixes(self, query: str) -> str:
        return '\n'.join(self.PREFIXES) + query
        
    def create_results_table(self, column_names: list[str], data = list[list]) -> None:
        result_win = tk.Tk()
        result_win.title("Результаты запроса")
        
        tree = ttk.Treeview(result_win, columns=column_names, show='headings')

        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill='both')
        
    def create_results_text(self, data: list[list]) -> None:
        result_win = tk.Tk()
        result_win.title("Результаты запроса")
        
        result_txt = st.ScrolledText(result_win)
        result_txt.pack(expand=True, fill='both')
        result_txt.insert(
            '1.0', 
            "\n".join(
                (" | ".join(map(str, row)) for row in data)
            )
        )
        
    def run(self) -> None:
        self.root.mainloop()
    

if __name__ == "__main__":
    App().run()
