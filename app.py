import tkinter as tk
import tkinter.ttk as ttk
import tkinter.scrolledtext as st
import tkinter.messagebox as msg

from rdflib import Graph


class App:
    GRAPH_IRI: str = "./resources/ecology.rdf"
    PREFIXES: tuple[str] = (
        "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>",
        "PREFIX owl: <http://www.w3.org/2002/07/owl#>",
        "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>",
        "PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>",
        "PREFIX ont: <http://www.semanticweb.org/egorp/ontologies/2024/11/untitled-ontology-20#>"    
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
            ?материал ont:Материал_активиста ?автор .
        }
            WHERE {
                ?материал ont:Название_материала ?название .
                ?материал ont:Материал_активиста ?автор .
            }
        """,
        "ASK" : """
        ASK {
            ?активист ont:ФИО_активиста "Кубанин Андрей Анатольевич" .
        }
        """
    }
    
    def __init__(self):
        self.graph = Graph()
        self.graph.parse(self.GRAPH_IRI)
        
        self.root = tk.Tk()
        self.root.title("Охрана Природы")
        
        self.set_query_field()
    
        self.set_predefined()
        
    def set_query_field(self) -> None:
        frame = ttk.Frame(self.root)
        frame.pack(side="top")
        
        self.query_field = st.ScrolledText(
            frame, 
            height=10
        )
        self.query_field.grid(row=0, column=1, rowspan=3, padx=10, pady=10)
        
        ttk.Button(
            frame, 
            text="Выполнить запрос",
            command=lambda: self.execute_query(self.query_field.get("1.0", tk.END).strip())
        ).grid(row=0, column=0, padx=10, pady=10)
        
        ttk.Button(
            frame, 
            text="Очистить поле",
            command=self.clear_query
        ).grid(row=1, column=0, padx=10, pady=10)
        
    
    def clear_query(self) -> None:
        self.query_field.delete("1.0", tk.END)
        
        
    def set_predefined(self) -> None:
        frame = ttk.Frame(self.root)
        frame.pack(side="top")
        
        for title, query in self.QUERIES.items():
            ttk.Button(
                frame, 
                text=title,
                command=lambda q=query: self.query_field.insert('1.0', q.strip())
            ).pack(side='left', padx=5, pady=5)
        
    def create_results_table(self, column_names: None, data: None) -> None:
        result_win = tk.Tk()
        result_win.title("Результаты запроса")
        
        tree = ttk.Treeview(result_win, columns=column_names, show='headings')

        for col in column_names:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in data:
            tree.insert("", "end", values=row)

        tree.pack(expand=True, fill='both')

    def execute_query(self, query: str) -> None:
        if not query:
            msg.showwarning("Ошибка", "Поле запроса пустое")
            return
        try:
            results = self.graph.query(
                self.add_prefixes(query)
            )
            parsed_data = [] 
            for row in results:
                parsed_data.append([row.get(var) for var in results.vars])
            
            self.create_results_table(
                column_names=results.vars,
                data=parsed_data
            )
        except Exception as e:
            msg.showerror("Ошибка", str(e))
            
    def add_prefixes(self, query: str) -> str:
        return '\n'.join(self.PREFIXES) + query

    def run(self) -> None:
        self.root.mainloop()



if __name__ == "__main__":
    App().run()
